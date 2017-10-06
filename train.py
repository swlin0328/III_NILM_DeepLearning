#!/usr/bin/env python


from __future__ import print_function, division

import os
import argparse
import importlib
from time import strftime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from neuralnilm.data.loadactivations import load_nilmtk_activations
from neuralnilm.data.syntheticaggregatesource import SyntheticAggregateSource
#from neuralnilm.data.realaggregatesource import RealAggregateSource
#from neuralnilm.data.stridesource import StrideSource
from neuralnilm.data.datapipeline import DataPipeline
from neuralnilm.data.processing import DivideBy, IndependentlyCenter
from neuralnilm.utils import select_windows, filter_activations

from lib import dirs
from dataprocess import realaggregatesource 
from dataprocess import stridesource
# Config
WINDOWS = None
BUILDINGS = None
SEQ_PERIODS = None


# Parameters
DATASET = None
NILMTK_FILENAME = None
TARGET_APPLIANCE = None
SAMPLE_PERIOD = None
NUM_STEPS = None
TOPOLOGY_NAME = None
OVERRIDE = None


# Constants
NUM_SEQ_PER_BATCH = 24
BRIEFING_NUM_STEPS = 1000


# Main
def main():
    set_log_level()
    parse_args()
    load_config()

    # load the activations
    print('Loading activations ...')
    activations = load_nilmtk_activations(
        appliances=[TARGET_APPLIANCE],
        filename=NILMTK_FILENAME,
        sample_period=SAMPLE_PERIOD,
        windows=WINDOWS
    )

    # generate pipeline
    pipeline, input_std, target_std = get_pipeline(activations)

    # determine the input shape
    print('Determining input shape ... ', end='')
    batch = pipeline.get_batch()
    input_shape = batch.input.shape[1:]
    print(input_shape)

    # look for an existing model only when OVERRIDE is not on; if none, then
    # build a new one
    print('Looking for an existing model ... ', end='')
    model_filename = os.path.join(dirs.MODELS_DIR, DATASET + '_' + TARGET_APPLIANCE + '_' + strftime('%Y-%m-%d_%H_%m') + '.h5')
    if not OVERRIDE and os.path.exists(model_filename):
        print('Found; loading it ...')
        from keras.models import load_model
        model = load_model(model_filename)
    else:
        if OVERRIDE:
            print('Overridden; building a new one with the specified topology ...')
        else:
            print('Not found; building a new one with the specified topology ...')

        # define accuracy
        #import keras.backend as K
        #ON_POWER_THRESHOLD = DivideBy(target_std)(10)
        #def acc(y_true, y_pred):
        #    return K.mean(K.equal(K.greater_equal(y_true, ON_POWER_THRESHOLD),
        #                          K.greater_equal(y_pred, ON_POWER_THRESHOLD)))

        # build model
        topology_module = importlib.import_module(dirs.TOPOLOGIES_DIR + '.' + TOPOLOGY_NAME, __name__)
        model = topology_module.build_model(input_shape)
        print (model.summary())

    # train
    print('Preparing the training process ...')
    train(pipeline, model)

    # save the model
    print('Saving the model to ' + model_filename + ' ...')
    model.save(model_filename)


# Argument parser
def parse_args():
    global DATASET, NILMTK_FILENAME, TARGET_APPLIANCE
    global SAMPLE_PERIOD, NUM_SEQ_PER_BATCH, NUM_STEPS
    global BRIEFING_NUM_STEPS, TOPOLOGY_NAME, OVERRIDE

    parser = argparse.ArgumentParser()

    # required
    required_named_arguments = parser.add_argument_group('required named arguments')
    required_named_arguments.add_argument('-d', '--dataset',
                                          help='Dataset\'s name. For example, \'redd\'.',
                                          required=True)
    required_named_arguments.add_argument('-a', '--target-appliance',
                                          help='Target appliance. For example, \'fridge\'.',
                                          required=True)
    required_named_arguments.add_argument('-s', '--sample-period',
                                          help='Sample period (in seconds).',
                                          type=int,
                                          required=True)
    required_named_arguments.add_argument('-t', '--num-steps',
                                          help='Number of steps.',
                                          type=int,
                                          required=True)
    required_named_arguments.add_argument('-m', '--topology-name',
                                          help='Topology\'s name. For example, \'dae\'.',
                                          required=True)

    # optional
    optional_named_arguments = parser.add_argument_group('optional named arguments')
    optional_named_arguments.add_argument('-o', '--override',
                                          help='Flag to override existing model (if there\'s one).',
                                          action='store_true')

    # start parsing
    args = parser.parse_args()

    DATASET = args.dataset
    NILMTK_FILENAME = os.path.join(dirs.DATA_DIR, DATASET + '.h5')
    TARGET_APPLIANCE = args.target_appliance
    SAMPLE_PERIOD = args.sample_period
    NUM_STEPS = args.num_steps
    TOPOLOGY_NAME = args.topology_name

    OVERRIDE = args.override


# Config loader
def load_config():
    global WINDOWS, BUILDINGS, SEQ_PERIODS

    # dataset-dependent config
    config_module = importlib.import_module(dirs.CONFIG_DIR + '.' + DATASET, __name__)
    WINDOWS = config_module.WINDOWS
    BUILDINGS = config_module.BUILDINGS

    # sequence periods (shared among datasets)
    seq_periods_module = importlib.import_module(dirs.CONFIG_DIR + '.seq_periods', __name__)
    SEQ_PERIODS = seq_periods_module.SEQ_PERIODS


# Pipeline
def get_pipeline(activations):
    # sequence periods
    seq_period = SEQ_PERIODS[TARGET_APPLIANCE]
    seq_length = seq_period // SAMPLE_PERIOD

    # buildings
    buildings = BUILDINGS[TARGET_APPLIANCE]
    train_buildings = buildings['train_buildings']
    unseen_buildings = buildings['unseen_buildings']

    # windows
    filtered_windows = select_windows(
        train_buildings, unseen_buildings, WINDOWS)
    filtered_activations = filter_activations(
        filtered_windows, activations, [TARGET_APPLIANCE])

    # data sources
    synthetic_agg_source = SyntheticAggregateSource(
        activations=filtered_activations,
        target_appliance=TARGET_APPLIANCE,
        seq_length=seq_length,
        sample_period=SAMPLE_PERIOD
    )
    real_agg_source = realaggregatesource.RealAggregateSource(
        activations=filtered_activations,
        target_appliance=TARGET_APPLIANCE,
        seq_length=seq_length,
        filename=NILMTK_FILENAME,
        windows=filtered_windows,
        sample_period=SAMPLE_PERIOD
    )
    stride_source = stridesource.StrideSource(
        target_appliance=TARGET_APPLIANCE,
        seq_length=seq_length,
        filename=NILMTK_FILENAME,
        windows=filtered_windows,
        sample_period=SAMPLE_PERIOD,
        stride=None
    )

    # look for existing processing parameters only when OVERRIDE is not on; if
    # none, generate new ones
    print('Looking for existing processing parameters ... ', end='')
    proc_params_filename = os.path.join(dirs.MODELS_DIR, 'proc_params_' + DATASET + '_' + TARGET_APPLIANCE + '_' + strftime('%Y-%m-%d_%H_%m') + '.npz')
    if not OVERRIDE and os.path.exists(proc_params_filename):
        print('Found; using them ...')
        input_std, target_std = np.load(proc_params_filename)['arr_0']
    else:
        if OVERRIDE:
            print('Overridden; generating new ones ...')
        else:
            print('Not found; generating new ones ...')
        sample = real_agg_source.get_batch(num_seq_per_batch=1024).next()
        sample = sample.before_processing
        input_std = sample.input.flatten().std()
        target_std = sample.target.flatten().std()

        print('Saving the processing parameters ...')
        np.savez(proc_params_filename, [input_std, target_std])

    # generate pipeline
    pipeline = DataPipeline(
        [synthetic_agg_source, real_agg_source, stride_source],
        num_seq_per_batch=NUM_SEQ_PER_BATCH,
        input_processing=[DivideBy(input_std), IndependentlyCenter()],
        target_processing=[DivideBy(target_std)]
    )

    return pipeline, input_std, target_std


# Trainer
def train(pipeline, model):
    # create output directory
    print('Creating output directory ... ', end='')
    output_dir = os.path.join( dirs.OUTPUT_DIR,
                              DATASET + '_' + TARGET_APPLIANCE + '_' + strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(output_dir)
    print(output_dir)

    # generate validation batch and create output sub-directories for each of them
    valid_batch = pipeline.get_batch(fold='unseen_activations_of_seen_appliances',
                                     reset_iterator=True,
                                     validation=True)
    valid_sample_indices = np.random.choice(range(NUM_SEQ_PER_BATCH), size=10, replace=False)
    for i in range(1, valid_sample_indices.shape[0] + 1):
        os.makedirs(os.path.join(output_dir, str(i)))

    # run
    log = []
    for step in range(NUM_STEPS + 1):
        # generate batch
        batch = pipeline.get_batch()
        while batch is None:
            batch = pipeline.get_batch()

        # train on a single batch (except for step 0, so that the code below can
        # generate briefing on the initial state of the model at step 0)
        if (step != 0):
            train_metrics = model.train_on_batch(batch.input, batch.target)

        # generate briefing
        if (step % BRIEFING_NUM_STEPS == 0 or step == NUM_STEPS):
            prediction = model.predict_on_batch(valid_batch.input)
            valid_metrics = model.evaluate(valid_batch.input, valid_batch.target, verbose=0)

            for sample_no, sample_index in enumerate(valid_sample_indices):
                p1 = plt.subplot(131)
                p1.set_title('Input #{}'.format(sample_no + 1))
                p2 = plt.subplot(132, sharey=p1)
                p2.set_title('Target #{}'.format(sample_no + 1))
                p3 = plt.subplot(133, sharey=p1)
                p3.set_title('Prediction #{}'.format(sample_no + 1, step))
                p1.plot(valid_batch.before_processing.input[sample_index].flatten())
                p2.plot(valid_batch.before_processing.target[sample_index].flatten())
                p3.plot(pipeline.apply_inverse_processing(prediction[sample_index], 'target').flatten())
                plt.savefig(os.path.join(output_dir, str(sample_no + 1), 'Step_{}.png'.format(step)))
                plt.clf()

            if (step == 0):
                print('===============================================================================')
                print('============================== Start of training ==============================')
                print('===============================================================================')
            else:
                print('Step {}:'.format(step))
                print('  Training metrics: ', end='')
                for i, metrics_name in enumerate(model.metrics_names):
                    print('{}={:.4f}, '.format(metrics_name, train_metrics[i]), end='')
                print('')
                print('  Validation metrics: ', end='')
                for i, metrics_name in enumerate(model.metrics_names):
                    print('{}={:.4f}, '.format(metrics_name, valid_metrics[i]), end='')
                print('')

                # append to log
                log.append([step] + train_metrics + valid_metrics)

    print('===============================================================================')
    print('=============================== End of training ===============================')
    print('===============================================================================')

    # write the log
    print('Writing log ...')
    log_df = pd.DataFrame(log, columns=(['step'] +
                                        ['train_'+metrics_name for metrics_name in model.metrics_names] +
                                        ['valid_'+metrics_name for metrics_name in model.metrics_names]))
    log_df.to_csv(os.path.join(output_dir, 'log_' + TARGET_APPLIANCE + '_' + strftime('%Y-%m-%d_%H_%m') + '.csv'), index=False, float_format='%.4f')

def set_log_level():
    # hide warning log
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # ignore UserWarning log
    import warnings
    warnings.filterwarnings("ignore")

if __name__ == '__main__':
    main()

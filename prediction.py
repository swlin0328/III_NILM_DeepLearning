#!/usr/bin/env python


from __future__ import print_function, division

import os
import argparse
import importlib
from time import strftime

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import load_model

from lib import dirs
from keras import backend as K
# Config
APPLIANCES = None
APPLIANCES_ATTRIBUTES = None

# Parameters
AGGREGATE_FILENAME = None
TARGET_FILENAME  = None
TARGET_APPLIANCE = None
MODEL_FILENAME = None
SEQ_LENGTH = None
DATA_LENGTH = None

# Content
NUM_SEQ_PER_BATCH = 24



# Main
def main():
    set_log_level()
    #set_keras_backend("theano")
    parse_args() 
    loss_score=Prediction_Evaluate()
    loss_score=pd.DataFrame(loss_score)
    loss_score.to_csv(os.path.join(dirs.DATA_DIR,'test_result_' + strftime('%Y-%m-%d_%H-%M-%s')+'.txt'))
    # print loss score
    #print ('loss_score:', loss_score)
    print('Accuracy:', loss_score[0][1] * 100, '%')
    #set_keras_backend("tensorflow")
    print('Done!')
 

# Argument parser
def parse_args():
    global AGGREGATE_FILENAME, TARGET_FILENAME, TARGET_APPLIANCE, MODEL_FILENAME 

    parser = argparse.ArgumentParser()
    required_named_arguments = parser.add_argument_group('required named arguments')
    required_named_arguments.add_argument('-d', '--datasetaggregate',
                                          help='Dataset\'s name. For example, \'aggregate\'.',
                                          required=True)
    required_named_arguments.add_argument('-t', '--datasettarget',
                                          help='Dataset\'s name. For example, \'fridge\'.',
                                          required=True)
    required_named_arguments.add_argument('-a', '--targetappliance',
                                          help='Target appliance. For example, \'fridge\'.',
                                          type=int,
                                          required=True) 
    # optional
    optional_named_arguments = parser.add_argument_group('optional named arguments')
    optional_named_arguments.add_argument('-m', '--model',
                                          help='Flag to call a specific model.')

    args = parser.parse_args()
    DATASET_AGGREGATE = args.datasetaggregate
    AGGREGATE_FILENAME = os.path.join( dirs.DATA_DIR, DATASET_AGGREGATE+'.csv')
    DATASET_TARGET = args.datasettarget
    TARGET_FILENAME = os.path.join( dirs.DATA_DIR, DATASET_TARGET+'.csv')

    target_appliance = args.targetappliance
    TARGET_APPLIANCE = RENAME(target_appliance)
    MODEL=args.model

    if  MODEL==None:
        MODEL_FILENAME= os.path.join( dirs.MODELS_DIR, TARGET_APPLIANCE + '.h5')
        print(MODEL_FILENAME)
    else :
        MODEL_FILENAME= os.path.join( dirs.MODELS_DIR, MODEL + '.h5')
        print(MODEL_FILENAME)
    

# Prediction_Evaluate
def Prediction_Evaluate():

    # load the prediction raw data
    print('Loading data...')
    df_aggregate = pd.DataFrame(np.zeros(DATA_LENGTH),columns=['w'])
    df_target = pd.DataFrame(np.zeros(DATA_LENGTH),columns=['w'])
    df_aggregate['w'] = pd.read_csv(AGGREGATE_FILENAME)['w'][0:DATA_LENGTH]
    df_target['w'] = pd.read_csv(TARGET_FILENAME)['w'][0:DATA_LENGTH]
    df_aggregate = df_aggregate.fillna(0)
    df_target = df_target.fillna(0)

    # reshape the prediction raw data
    df_aggregate=df_aggregate['w'].values.reshape(NUM_SEQ_PER_BATCH,SEQ_LENGTH,1)
    df_target=df_target['w'].values.reshape(NUM_SEQ_PER_BATCH,SEQ_LENGTH,1)

    # load model
    model=load_model(MODEL_FILENAME)
    loss_score=model.evaluate(df_aggregate, df_target, verbose=0)
    
    # generate briefing
    prediction = model.predict_on_batch(df_aggregate)
    prediction_sample_indices = np.random.choice(range(NUM_SEQ_PER_BATCH), size=5, replace=False)

    print('Creating test result csv ... \n', end='')
    output_dir = os.path.join(dirs.OUTPUT_DIR,'test_result_' + strftime('%Y-%m-%d_%H-%M-%s'))
    os.makedirs(output_dir)

    for sample_no, sample_index in enumerate(prediction_sample_indices):
        p1 = plt.subplot(131)
        p1.set_title('Input #{}'.format(sample_no + 1))
        p2 = plt.subplot(132, sharey=p1)
        p2.set_title('Target #{}'.format(sample_no + 1))
        p3 = plt.subplot(133, sharey=p1)
        p3.set_title('Prediction #{}'.format(sample_no + 1))
        p1.plot(df_aggregate[sample_index].flatten())
        p2.plot(df_target[sample_index].flatten())
        p3.plot(prediction[sample_index].flatten())
        plt.savefig(output_dir+'/test_#{}.png'.format(sample_no + 1))
        plt.clf()  
        
    prediction=pd.DataFrame(prediction.reshape(DATA_LENGTH,1)) 
    prediction.to_csv(os.path.join( output_dir,  'prediction_value' +'.csv'))

    return loss_score

def RENAME(target_appliance):
    global SEQ_LENGTH, DATA_LENGTH
    SEQ_LENGTH = 60
    DATA_LENGTH = 1440

    if target_appliance == 0002 :
        target_appliance = 'television' 

    if target_appliance == 0003 :
        target_appliance = 'fridge' 
    
    if target_appliance == 0004 :
        target_appliance = 'air_conditioner'
        SEQ_LENGTH = 60
        DATA_LENGTH = 1440

    if target_appliance == 0005 :
        target_appliance = 'bottle_warmer'

    if target_appliance == 0006 :
        target_appliance = 'washing_machine'
        
    return target_appliance

def set_log_level():
    # hide warning log
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # ignore UserWarning log
    import warnings
    warnings.filterwarnings("ignore")

def set_keras_backend(backend):
    
    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        reload(K)
        assert K.backend() == backend

if __name__ == '__main__':
    main()

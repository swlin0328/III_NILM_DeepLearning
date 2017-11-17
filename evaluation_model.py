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

# Config
SEQ_LENGTH = 60
num_batch = None
date_agg = None
date_each = None

def eval(model_name):
    set_log_level()
    MODEL_FILENAME = os.path.join( 'models', model_name+'.h5' )
    print(MODEL_FILENAME)
    model=load_model(MODEL_FILENAME)
    print('model summary')
    print(model.summary())
    print('loading data..')
    df_agg, df_each = load_data(date_agg, data_each)
    # Normalized
    mean_agg = df_agg.mean(axis=1,keepdims=True)
    std_agg = mean_agg.flatten().std()
    df_agg_normalized = (df_agg-mean_agg)/std_agg

    mean_each = df_each.mean(axis=1,keepdims=True)
    std_each = mean_each.flatten().std()
    df_each_normalized = df_each/std_each
       
    eval = model.predict_on_batch(df_agg_normalized)
    eval = eval*std_each
    valid_metrics = model.evaluate(df_agg_normalized, df_each_normalized , verbose=0)

    # save
    print('Creating test result ... \n', end='')
    output_dir = os.path.join('eval', model_name )
    if not os.path.exists(output_dir ):
        os.makedirs(output_dir)

    sample_indices = np.random.choice(range(num_batch), size=20, replace=False)
    
    for sample_no, sample_index in enumerate(sample_indices):
        p1 = plt.subplot(131)
        p1.set_title('Input #{}'.format(sample_no + 1))
        p2 = plt.subplot(132, sharey=p1)
        p2.set_title('Target #{}'.format(sample_no + 1))
        p3 = plt.subplot(133, sharey=p1)
        p3.set_title('Prediction #{}'.format(sample_no + 1))
        p1.plot(df_agg[sample_index])
        p2.plot(df_each[sample_index])
        p3.plot(eval[sample_index])
        plt.savefig(os.path.join(output_dir, 'result#{}.png'.format(sample_no + 1)))
        plt.clf()
    
    for i, metrics_name in enumerate(model.metrics_names):
        print('{}={:.4f}, '.format(metrics_name, valid_metrics[i]), end='')
        print('')  

    loss_score=pd.DataFrame(valid_metrics)
    loss_score.to_csv(os.path.join(output_dir, 'lost_score' +'.csv'))
    with open(os.path.join(output_dir)+'/summary.txt','w') as f:
        model.summary(print_fn=lambda x: f.write(x + '\n'))


def load_data(data_agg, data_each):
    global num_batch
    data_agg = os.path.join( 'data', 'predict', data_agg + '.dat' )
    data_each = os.path.join( 'data', 'predict',data_each + '.dat' )
    data_agg = pd.read_csv(data_agg)
    data_each = pd.read_csv(data_each)
    data_length = len(data_each.iloc[:,0])
    num_batch = data_length//SEQ_LENGTH
    length = SEQ_LENGTH*num_batch
    df_agg = data_agg.iloc[0:length,1]
    df_each = data_each.iloc[0:length,1]
    df_agg= df_agg.reshape(num_batch,SEQ_LENGTH,1)
    df_each= df_each.reshape(num_batch,SEQ_LENGTH,1)
    return df_agg, df_each

    
def set_log_level():
    # hide warning log
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # ignore UserWarning log
    import warnings
    warnings.filterwarnings("ignore")

if __name__ == '__main__':
    date_agg = 'channel_1'
    data_each = 'channel_4'
    for model in ["HEMS_PongHu2017-11-03_fridge_2017-11-15_14_11"]:
    #                'HEMS_PongHu2017-11-03_fridge_2017-11-06_11_11',
    #                'HEMS_PongHu2017-11-03_fridge_2017-11-05_21_11',
    #                'HEMS_PongHu2017-11-03_fridge_2017-11-04_15_11']:
        eval(model)
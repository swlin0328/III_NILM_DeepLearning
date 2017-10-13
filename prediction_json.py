#!/usr/bin/env python

from __future__ import print_function, division

import os
import argparse
from lib import dirs
from time import strftime

import requests
import numpy as np
import pandas as pd

#from keras.models import load_model

# for json
import io
import json
import urllib2
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

from keras import backend as K


# Parameters

RAW_DATA_LIST = None
APPLIANCE_TYPE = None
MODEL_FILENAME = None

SEQ_LENGTH = 60

### main ###
def main():
    set_keras_backend("theano")
    set_log_level()
    parse_args() 
    Prediction_Evaluate()
    set_keras_backend("tensorflow")
    print('Done !')

### arse_args ###
def parse_args():
    global  RAW_DATA_LIST, APPLIANCE_TYPE, MODEL_FILENAME
    parser = argparse.ArgumentParser()
    required_named_arguments = parser.add_argument_group('required named arguments')
    required_named_arguments.add_argument('-u', '--url',
                                          help='url',
                                          required=True)
    # optional
    optional_named_arguments = parser.add_argument_group('optional named arguments')
    optional_named_arguments.add_argument('-m', '--model',
                                          help='Flag to call a specific model.')

    args = parser.parse_args()
    url = args.url
    URL = json.load(urllib2.urlopen(url))
    RAW_DATA_LIST = URL['raw_data_list']
    appliance_type = str(URL['appliance_type'])
    APPLIANCE_TYPE = RENAME(appliance_type)
    MODEL = args.model

    if  MODEL== None:
        MODEL_FILENAME= os.path.join( dirs.MODELS_DIR, APPLIANCE_TYPE + '.h5')
    else :
        MODEL_FILENAME= os.path.join( dirs.MODELS_DIR, MODEL + '.h5')
        

### RENAME ###
def RENAME(target_appliance):
    if target_appliance == '0002' :
        target_appliance = 'television' 

    if target_appliance == '0003' :
        target_appliance = 'fridge' 
    
    if target_appliance == '0004' :
        target_appliance = 'air_conditioner'

    if target_appliance == '0005' :
        target_appliance = 'bottle warmer' 

    if target_appliance == '0006' :
        target_appliance = 'washing machine' 

    return target_appliance


### Prediction_Evaluate ###
def Prediction_Evaluate():

    # load the prediction raw data
    print('Loading data...')
    NUM_SEQ_PER_BATCH = len(RAW_DATA_LIST)//SEQ_LENGTH
    L = NUM_SEQ_PER_BATCH*SEQ_LENGTH
    df_aggregate = pd.DataFrame(np.zeros(L),columns=['w'])
    df_aggregate['w'][0:L] = RAW_DATA_LIST[0:L]
    df_aggregate = df_aggregate.fillna(0)
    df_aggregate=df_aggregate['w'].reshape(NUM_SEQ_PER_BATCH,SEQ_LENGTH,1)

    # Keras..
    from keras.models import load_model
    model=load_model(MODEL_FILENAME)
    prediction = model.predict_on_batch(df_aggregate)

    # Saving...
    print('Creating test result ... \n', end='')
    output_dir = os.path.join(dirs.OUTPUT_DIR,'test_result_' + strftime('%Y-%m-%d_%H-%M-%s'))
    os.makedirs(output_dir)
    prediction = prediction.reshape(L,1)
    prediction = prediction.tolist()
 

    APPLIANCE_USAGE = { "Appliance_usage": prediction }
    print('Saving in Json file...')
    with io.open( os.path.join(output_dir,'Appliance_usage.json') ,'w' ,encoding='utf8') as outfile:
        str_ = json.dumps(APPLIANCE_USAGE)
        outfile.write(to_unicode(str_))
    # delete the existing model
    print ('Deleting the existing model...')
    del model 

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


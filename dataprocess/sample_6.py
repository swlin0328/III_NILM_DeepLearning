#!/usr/bin/env python

import nilmtk
import pandas as pd
import numpy as np
from neuralnilm.utils import check_windows
from copy import copy
import random
from datetime import timedelta
from neuralnilm.data.source import Sequence
from neuralnilm.data.activationssource import ActivationsSource
from neuralnilm.consts import DATA_FOLD_NAMES

import logging
logger = logging.getLogger(__name__)


class Sample(ActivationsSource):
    def __init__(self, activations, target_appliance,
                 seq_length, filename, windows, sample_period,
                 uniform_prob_of_selecting_each_building=True,
                 allow_incomplete_target=True,
                 rng_seed=None):
        
        self.activations = copy(activations)
        self.target_appliance = target_appliance
        self.seq_length = seq_length
        self.filename = filename
        check_windows(windows)
        self.windows = windows
        self.sample_period = sample_period

        self.uniform_prob_of_selecting_each_building=(
            uniform_prob_of_selecting_each_building)
        self.allow_incomplete_target = allow_incomplete_target
        super(Sample, self).__init__(rng_seed=rng_seed)
        self._load_mains_into_memory()
        self.target_inclusion_prob=0.5
        

    def _load_mains_into_memory(self):
        logger.info("Loading NILMTK mains...")

        # Load dataset
        dataset = nilmtk.DataSet(self.filename)
        self.dataset = dataset
        self.mains = {}
        self.fridge = {}
        self.AC = {}
        for fold, buildings_and_windows in self.windows.iteritems():
            for building_i, window in buildings_and_windows.iteritems():
                dataset.set_window(*window)
                elec = dataset.buildings[building_i].elec
                building_name = (dataset.metadata['name'] +'_building_{}'.format(building_i))

                logger.info(
                    "Loading mains for {}...".format(building_name))

                mains_meter = elec.mains()
                mains_data = mains_meter.power_series_all_data(sample_period=self.sample_period).dropna()#,
                    #sections=good_sections).dropna()
                fridge_data = elec['fridge'].power_series_all_data(sample_period=self.sample_period).dropna()
                AC_data = elec['air conditioner'].power_series_all_data(sample_period=self.sample_period).dropna()

                def set_mains_data(dictionary, data):
                    dictionary.setdefault(fold, {})[building_name] = data

                if not mains_data.empty:
                    set_mains_data(self.mains, mains_data)
                    set_mains_data(self.fridge, fridge_data)
                    set_mains_data(self.AC, AC_data)

                logger.info(
                    "Loaded mains data from building {} for fold {}"
                    " from {} to {}."
                    .format(building_name, fold,
                            mains_data.index[0], mains_data.index[-1]))

        dataset.store.close()
        logger.info("Done loading NILMTK mains data.")

    def get_main_fridge(self, fold='train'):

        building_number = random.randint(1,len(self.mains[fold].keys()))
        build_name = sorted(self.mains[fold].keys())[building_number-1]
        main_data = self.mains[fold][build_name]
        fridge_data = self.fridge[fold][build_name]
        # start time point can be any point in main except for the last seq_length ones
        start = main_data[:-self.seq_length].sample(n=1).index[0]
        end = start + timedelta(seconds = self.seq_length* (self.sample_period-1))
        success = False
        while not success  : 
            if len(fridge_data[start:end])!=self.seq_length or
                    len(main_data[start:end])!=self.seq_length or 
                    fridge_data[start:end].sum()<=50:
                main_data = self.mains[fold][build_name]
                start = main_data[:-self.seq_length].sample(n=1).index[0]
                end = start + timedelta(seconds = self.seq_length* (self.sample_period-1))
            else:
                success = True
                                   
        seq = Sequence(self.seq_length)
        seq.input = np.pad( main_data[start:end], (self.seq_length-len(main_data[start:end])), 'constant')
        seq.target = np.pad( fridge_data[start:end], (self.seq_length-len(main_data[start:end])), 'constant')
        return seq

    def _get_sequence(self, fold='train', enable_all_appliances=False):
        seq = self.get_main_fridge(fold=fold)
        return seq
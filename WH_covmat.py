"""
=========================================================
WH: make covariance matrices from epoched baselines
OH May 2017
=========================================================

"""

import os
import os.path as op
import sys

import importlib

# import matplotlib
# matplotlib.use('Agg') # possibly for running on cluster

import matplotlib.pyplot as plt
import numpy as np

from copy import deepcopy

import mne

print(__doc__)

## get analysis parameters from config file
if len(sys.argv)>1:
    print sys.argv[1]
    module_name = sys.argv[1]
else:
    module_name = 'WH_config'

C = importlib.import_module(module_name)
reload(C)

# plt.ion() # interactive plotting

# subject numbers
subjs  = C.subjs

# for qsub
if len(sys.argv)>2: # if in parallel mode
    print "Running subject(s) {0} now in PARALLEL mode".format(sys.argv)
    ss_idx = map(int, sys.argv[2:])
    subjs_new = []
    for ii,ss in enumerate(ss_idx): # a bit cumbersome because lists cannot be used as indices
        subjs_new.append(subjs[ss])
    subjs = subjs_new
else:
    print "Running now in SERIAL mode"


for [si,sbj] in enumerate(subjs):
    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.cov_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:

        for origin in C.MF['origin']:

            for latwin in C.cov_latwins:

                ## read epochs
                epo_fname = C.fname_epo(C, subject, st_duration, origin)
                print('Reading epochs from %s.' % epo_fname)
                
                epochs = mne.read_epochs(epo_fname, preload=True)            

                # compute covariance matrix or matrices (output will be list)
                noise_covs = mne.compute_covariance(epochs, tmin=latwin[0], tmax=latwin[1],
                                        method=C.cov_methods, return_estimators=True)
                
                for [ci,cov] in enumerate(noise_covs):                    

                    cov_fname = C.fname_cov(C, subject, st_duration, origin, latwin, cov['method'], ci)

                    print('Writing covariance matrix to %s' % cov_fname)
                    
                    cov.save(cov_fname)
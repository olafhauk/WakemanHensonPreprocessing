"""
=========================================================
WH: plot covariance matrices
OH May 2017
=========================================================

"""

import os
import os.path as op
import sys

import importlib
import glob

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster

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

            ## read epochs
            epo_fname = C.fname_epo(C, subject, st_duration, origin)
            
            epochs = mne.read_epochs(epo_fname, preload=True)            

            for method in C.cov_methods: # doesn't work with 'auto'

                # covariance matrix (filter with wildcard)            
                cov_fname = C.fname_cov(C, subject, st_duration, origin, method, '*')

                # method may be underspecified, since it may be ranked differently for different subjects
                cov_fname = glob.glob(cov_fname)[0] # be careful if multiple options present

                cov = mne.read_cov(cov_fname)

                # hack to create filenames taking into account muliptle '.' in paths/names
                fstem = cov_fname.split('.')[0:-1] # remove suffix'
                fstem2 = ''.join([x+'.' for x in fstem[0:-1]]) # merge strings except last, insert '.'
                fstem2 = fstem2 + fstem[-1] # add last string without '.'

                fig_cov_fname = fstem2 + '.pdf'
                fig_spec_fname = fstem2 + 'spec.pdf'

                fig_cov, fig_spectra = mne.viz.plot_cov(cov, epochs.info, show=False)

                print('Plotting covariance matrix to\n%s\nand\n%s.\n' % (fig_cov_fname, fig_spec_fname))
                
                fig_cov.savefig(fig_cov_fname)

                fig_spectra.savefig(fig_spec_fname)                    

                plt.close('all')
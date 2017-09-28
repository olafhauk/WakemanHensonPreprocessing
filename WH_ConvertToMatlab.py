#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Average epochs -< evoked responses
==========================================

OH March 2017
"""
import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')

import os
from os import path as op

import importlib

import numpy as np

from scipy import io

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

###

n_sbs = len(subjs)

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

###############################################################################
# Load and filter data, create and save epochs
x = []
for [si,sbj] in enumerate(subjs):

    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.matlab_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:        

        for origin in C.MF['origin']:           

            ## read epochs
            epo_fname = C.fname_epo(C, subject, st_duration, origin)

            print 'Reading epochs from: %s' + epo_fname
            epochs = mne.read_epochs(epo_fname)
            
            ## get data matrices for Matlab
            epochs_mat = epochs.get_data()

            evoked_faces = epochs['fc'].average()
            faces = evoked_faces.data

            evoked_scrambled = epochs['sc'].average()
            scrambled = evoked_scrambled.data

            evoked_famous = epochs['fc/fm'].average()
            famous = evoked_famous.data

            evoked_unfamiliar = epochs['fc/uf'].average()
            unfamiliar = evoked_unfamiliar.data

            evoked_all = mne.combine_evoked([evoked_faces, evoked_scrambled], 'nave')
            ALL = evoked_all.data


            mat_fname = C.fname_matlab(C, subject, st_duration, origin)

            print('Saving data to: %s ' % mat_fname)

            to_save =   dict(
                                faces=faces,
                                scrambled=scrambled,
                                famous=famous,
                                unfamiliar=unfamiliar,
                                all=ALL,
                                epochs=epochs_mat,
                                times=epochs.times,
                                ch_names=epochs.info['ch_names'],
                                chs=epochs.info['chs'],
                                bads=epochs.info['bads'],
                                digs=epochs.info['dig']
                            )

            io.savemat(mat_fname, to_save)
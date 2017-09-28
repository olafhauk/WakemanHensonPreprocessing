#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
extract and write events from W&H EEG/MEG data
based on MNE-Python's demo 03-run_extract_events.py
==========================================

OH May 2017
"""
import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')

import os
import os.path as op
import matplotlib.pyplot as plt
import numpy as np

import importlib

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

# subject numbers (from Roni's Matlab script)
subjs  = C.subjs

# sessions per subject
sess = C.sess

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
    # if subsect of subjects specified; subject list start at 1

###############################################################################
# Load data, extract and write events

for [si,sbj] in enumerate(subjs):
    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.eve_mne_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:        

        for origin in C.MF['origin']:            

            for run in sess:                

                raw_fname, _ = C.fname_raw_out(C, subject, run, st_duration, origin)

                # file name to which to write event info
                eve_fname, _ = C.fname_eve(C, subject, run, st_duration, origin)

                print("Writing events to: %s" % eve_fname)

                print("processing subject: %s" % sbj)

                raw = mne.io.Raw(raw_fname)
                mask = 4096 + 256  # mask for excluding high order bits

                events = mne.find_events(raw, stim_channel='STI101',
                                   consecutive='increasing', mask=mask,
                                   mask_type='not_and', min_duration=0.003,
                                   verbose=True)

                print("Sub %s - Ses %s" % (sbj, run))

                mne.write_events(eve_fname, events)
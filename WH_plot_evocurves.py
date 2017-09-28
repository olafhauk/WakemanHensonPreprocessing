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

import importlib

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster

import os
import os.path as op
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

# identify epoch latencies in filename (no ".")
lat_tmp = str(int(1000*C.epo_t1)) + '_' + str(int(1000*C.epo_t2)) + "ms"
lat_str = lat_tmp.replace(".", "")

# identify filter in filename (no ".")
filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
filt_str = filt_tmp.replace(".", "")

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

for [si,sbj] in enumerate(subjs):

    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.evo_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:

        for origin in C.MF['origin']:       

            evo_fname = C.fname_evo(C, subject, st_duration, origin)
            
            evoked = mne.read_evokeds(evo_fname)

            for evo in evoked:

                fig = evo.plot(spatial_colors=True, window_title=evo.comment)

                fig_fname, _ = C.fname_fig_evo(C, subject, st_duration, origin, '', evo.comment)
                
                print("Saving figure to: %s " % fig_fname)
                fig.savefig(fig_fname)

                plt.close(fig)
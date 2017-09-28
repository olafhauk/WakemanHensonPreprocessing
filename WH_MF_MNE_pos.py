#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Create position files from Neuroimag Maxfilter
needed for MNE Maxfilter movement compensation
==========================================

OH July 2017
"""


import os
import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
# does this resolve the SVD problem??
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/envs/maxfilter_env/lib/python2.7/site-packages/')

import importlib

import os
import os.path as op
import numpy as np

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

# path to unmaxfiltered raw data
raw_path_in = C.raw_path_in

# output path for maxfiltered raw data
raw_path_sss = C.raw_path_sss

# subject numbers (from Roni's Matlab script)
subjs  = C.subjs

# sessions per subject
sess = C.sess
# sess = [1, 2]


###

n_sbs = len(subjs)
n_ses = len(sess)

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

# identify epoch latencies in filename (no ".")

        
###############################################################################
# 
for sbj in subjs:

    subject = 'Sub%02d' % sbj

    sub_dir = op.join(raw_path_sss, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)    

    for run in sess:

         # unmaxfiltered raw data
        raw_fname_in = C.fname_raw_in(C, subject, run)

        raw_fname_out = op.join(raw_path_sss, subject, 'tmp.fif') # dummy

        # prevents a warning message in err-files
        if os.path.exists(raw_fname_out):
            os.remove(raw_fname_out)
       
        pos_fname = C.fname_MF_pos(C, subject, run)

        mf_cmd = C.MF['NM_cmd'] + \
                    ' -f ' + raw_fname_in + \
                    ' -o ' + raw_fname_out + \
                    ' -headpos -hp ' + \
                    pos_fname + ' -force'

        print(mf_cmd)

        print("Saving positions to %s: \n" % pos_fname)

        os.system(mf_cmd)
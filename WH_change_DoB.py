#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Change DoB in my copy of WH data
test after talking to Russell about removing PID
!!! mne.io.write_info doesn't do what we want !!!
just a test
==========================================

OH March 2017
"""
import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/mne_python/v0.14/')

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster

import os.path as op
import matplotlib.pyplot as plt
import numpy as np

from copy import deepcopy

import mne
from mne.datasets import spm_face
from mne.preprocessing import ICA, create_eog_epochs
from mne import io, combine_evoked
from mne.minimum_norm import make_inverse_operator, apply_inverse

print(__doc__)

# plt.ion() # interactive plotting

# path to data set
data_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/RAW/'


# subject numbers (from Roni's Matlab script)
subjs  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# sessions per subject
sess = [1, 2, 3, 4, 5, 6]
# sess = [1, 2]

###

n_sbs = len(subjs)
n_ses = len(sess)


        
###############################################################################
# Load and filter data, create and save epochs
for [si,sbj] in enumerate(subjs):
    sbj_path = "/Sub" + "%.2d" % sbj

    for ses in sess:

        ## read and modify raw data

        raw_fname = data_path + sbj_path + "/run_" + "%.2d" % ses + "_sss.fif"
        print "Changing DoB for %s" % raw_fname

        # print raw_fname
        info = mne.io.read_info(raw_fname)

        info['subject_info']['birthday'] = (2017,4,1)

        mne.io.write_info(raw_fname, info)
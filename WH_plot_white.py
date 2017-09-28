"""
=========================================================
WH: plot whitened evoked data to check covariance matrices
OH May 2017
=========================================================

"""

print __doc__

import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/mne_python/v0.14/')

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster

import mne
import numpy as np

# path to output evoked responses
evo_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/AVG/'

# path to covariance matrices
cov_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/COV/'

# path to output covariance matrices
cov_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/COV/'

# path for figures
fig_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/Figures/'

# which channel types to process
pick_meg, pick_eeg, pick_eog = True, True, True


# Subject file information (ID, date, number, Go event)
# subject IDs
subjs  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

###
### the following is to choose filenames only

# latency interval for covariance
cov_t1, cov_t2 = -0.2, 0.0


# bandpass filter (Butterworth 4-th order)
h_freq = 40. # Hz
l_freq = 0.1

# compute separate covariance matrices for these methods:
methods = ['auto', 'empirical', 'ledoit_wolf', 'shrunk', 'pca']

# for filenames
lat_str_epo = "-200_400ms"
lat_str_cov = str(int(1000*cov_t1)) + '_' + str(int(1000*cov_t2))
filt_str = "01_400Hz"

# what type of events to read, MNE-Python demo ("MNE") or Wakeman&Henson ("WH")
# to choose filenames only, here not looped
event_def = "MNE"

# for qsub
if len(sys.argv)>1: # if in parallel mode
    print "Running subject(s) {0} now in PARALLEL mode".format(sys.argv)
    ss_idx = map(int, sys.argv[1:])
    subjs_new = []
    for ii,ss in enumerate(ss_idx): # a bit cumbersome because lists cannot be used as indices
        subjs_new.append(subjs[ss])
    subjs = subjs_new
else:
    print "Running now in SERIAL mode"


for sbj in subjs:
    subject = "Sub%.2d" % sbj
    print subject    

    evo_fname = evo_path + "evo_" + "%.2d" % sbj + "_" + lat_str_epo + "_" + filt_str + "_" + event_def + "-ave.fif"

    print("Reading evoked from %s: " % evo_fname)

    for method in methods:

        cov_fname = cov_path + '/' + subject + '_' + lat_str_cov + '_' \
                    + method + event_def + '-cov.fif'

        print "Reading covariance matrix from:" % cov_fname

        noise_cov = mne.read_cov(cov_fname)
    
        evo_fname = evo_path + "evo_" + "%.2d" % sbj + "_" + lat_str_epo + "_" + filt_str + "_" + event_def + "-ave.fif"
        print("Reading average from: %s " % evo_fname)
        evokeds = mne.read_evokeds(evo_fname)

        evoked = evokeds[0]

        fig = evoked.plot_white(noise_cov=noise_cov, show=True)

        fig_fname = fig_path + "white_" + "%.2d" % sbj + "_cov" + lat_str_cov + "_epo_" + lat_str_epo + "_" + filt_str + \
                        "_" + method + "_" + event_def + ".pdf"
        print("Saving figure to: %s " % fig_fname)
        fig.savefig(fig_fname)
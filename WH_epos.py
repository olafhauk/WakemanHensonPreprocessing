#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
filter raw data and create epochs
==========================================

OH July 2017
"""

# make sure correct events available (WH_extract_events.py)

import os
import os.path as op
import sys

import importlib

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

###
subjs = C.subjs
sess = C.sess

n_sbs = len(subjs)
n_ses = len(sess)

# bad EEG channels (from /imaging/rh01/Methods/DanData/Raw/SPMScripts/meeg_preproc.m)
# indices corrected by -1...
bad_EEG = [0]*16 # ALL SUBJECTS
bad_EEG[7]  = ['EEG034','EEG045','EEG056']
bad_EEG[8]  = ['EEG004','EEG043','EEG045','EEG047']
bad_EEG[11] = ['EEG016','EEG024','EEG029','EEG057']
bad_EEG[12] = ['EEG044']
bad_EEG[13] = ['EEG029']
bad_EEG[15] = ['EEG002','EEG004','EEG008']

bad_EEG[4] = ['EOG061'] # added by OH, EOG noisy, no ICA
bad_EEG[15].append('EOG062') # added by OH, EOG noisy, no ICA


# rename bipolar channels
rename_EEG = {'EEG061': 'EOG061', 'EEG062': 'EOG062', 'EEG063': 'ECG063'}
drop_EEG = ['EEG064'] # drop for all subjects

# for qsub
if len(sys.argv)>2: # if in parallel mode
    print "Running subject(s) {0} now in PARALLEL mode".format(sys.argv)
    ss_idx = map(int, sys.argv[2:])
    subjs_new = []
    bad_EEG_new = []
    for ii,ss in enumerate(ss_idx): # a bit cumbersome because lists cannot be used as indices
        subjs_new.append(subjs[ss])
        bad_EEG_new.append(bad_EEG[ss])
    subjs = subjs_new
    bad_EEG = bad_EEG_new
else:
    print "Running now in SERIAL mode"
    # if subsect of subjects specified; subject list start at 1
    bad_EEG = [bad_EEG[i-1] for i in subjs]
        
###############################################################################
# Load and filter data, create and save epochs
for [si,sbj] in enumerate(subjs):
    
    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.epo_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:

        for origin in C.MF['origin']:

            events_list = [] # list or events corresponding to raws

            epochs_ses = [] # list of epoch objects across sessions per subject

            for run in sess:            

                raw_fname, _ = C.fname_raw_out(C, subject, run, st_duration, origin)
              
                # events extracted by MNE
                eve_fname, fig_fname = C.fname_eve(C, subject, run, st_duration, origin)
                
                # print raw_fname
                raw = mne.io.read_raw_fif(raw_fname, preload=True)

                # without this, will complain for some subjects that epochs[5]['info']['dev_head_t']
                # must match
                raw.info['chs'][366]['coil_type'] = 5 # EOG
                raw.info['chs'][366]['kind'] = 202
                raw.info['chs'][367]['coil_type'] = 5
                raw.info['chs'][367]['kind'] = 202

                raw.info['chs'][368]['coil_type'] = 5 # ECG - not sure how to code it
                raw.info['chs'][368]['kind'] = 202

                raw.set_channel_types({'EEG061': 'eog',
                                   'EEG062': 'eog',
                                   'EEG063': 'ecg',
                                   'EEG064': 'misc'})  # EEG064 free floating el.
                raw.rename_channels({'EEG061': 'EOG061',
                                 'EEG062': 'EOG062',
                                 'EEG063': 'ECG063'})

                if type(bad_EEG[si]) != int: # if bad electrodes specified for this subject
                    print("Bad EEGs: %s" % bad_EEG[si] )
                    # raw.drop_channels(bad_EEG[si])
                    raw.info['bads'] = bad_EEG[si]
                    print(raw.info)

                # in order to keep bad EOGs, reset_bad=False
                raw.interpolate_bads(reset_bads=False)
                raw.set_eeg_reference()               

                ## bandpass filter raw data
                picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True)

                raw.filter(C.l_freq, C.h_freq, l_trans_bandwidth='auto', h_trans_bandwidth='auto',
                       filter_length='auto', phase='zero', fir_window='hann', fir_design='firwin')

                ## read event information from text file, convert to MNE format

                events = mne.read_events(eve_fname)

                delay = int(C.delay * raw.info['sfreq'])                

                # correct for stimulus presentation delay
                events[:, 0] = events[:, 0] + delay

                events_list.append(events)
                
                # plot the events to get an idea of the paradigm
                eve_fig = mne.viz.plot_events(events, raw.info['sfreq'])

                print("Saving figure to %s" % fig_fname)

                eve_fig.savefig(fig_fname)
                plt.close(eve_fig)

                epochs = mne.Epochs(raw=raw, events=events, event_id=C.event_id, tmin=C.epo_t1,
                                tmax=C.epo_t2, proj=True, picks=picks, baseline=C.epo_baseline, preload=True,
                                reject=C.reject)
                epochs_ses.append(epochs)

            ## concatenate eochs across sessions
            epochs = mne.concatenate_epochs(epochs_ses)
            
            epo_fname = C.fname_epo(C, subject, st_duration, origin)
           
            print("Saving epochs to %s" % epo_fname)
            epochs.save(epo_fname)
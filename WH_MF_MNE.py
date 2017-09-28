#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Try to read Wakeman/Henson EMEG data
WH_maxfilter [config file] [subjects]
can take list of st_duration
==========================================

OH July 2017
"""

# NOTE: CHeck C.MF_method"


import os
import sys
# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
# sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
# does this resolve the SVD problem??
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/envs/maxfilter_env/lib/python2.7/site-packages/')

import importlib

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

    # reference session for trans
    # using third run to make comparable to Neuromag maxfilter
    raw_fname_ref = C.fname_raw_in(C, subject, C.MF['ref_sess'])

    print('Using %s as reference file.' % raw_fname_ref)
    raw_ref = mne.io.read_raw_fif(raw_fname_ref)

    destination = raw_ref.info['dev_head_t']['trans'][:3, 3]

    for run in sess:

        raw_fname_in = C.fname_raw_in(C, subject, run)
        
        # check if readable
        try:
            raw = mne.io.read_raw_fif(raw_fname_in, preload=True)
        except AttributeError:
            # Some files on openfmri are corrupted and cannot be read.
            warn('Could not read file %s. '
                 'Skipping run %s from subject %s.' % (raw_fname_in, run, subject))
            continue

        # because of MNE warning
        raw.fix_mag_coil_types()

        # Hackish way of reading bad channels from the log.
        log_fname = op.join(raw_path_in, subject, 'MEEG', 'MaxFilterOutput', 'run_%.2d_sss_log.txt' % run)
        bads = []
        with open(log_fname) as fid:
            for line in fid:
                if line.startswith('Static bad channels'):
                    chs = line.split(':')[-1].split()
                    bads = ['MEG%04d' % int(ch) for ch in chs]
                    break

                    
            raw.info['bads'] += bads
            print("BAD CHANNELS:\n")
            print(raw.info['bads'])

        ## MAXFILTER
        for st_duration in C.MF['st_duration']:            

            for origin in C.MF['origin']:                

                # Movement compensation if appropriate
                if not(C.MF['mv']==''): # if movement compensation requested, create head 
                                        # positions using Neuromag Maxfilter
                    pos_fname = C.fname_MF_pos(C, subject, run)

                    head_pos = mne.chpi.read_head_pos(pos_fname)

                    if sbj in C.pos_correct[:,0]:
                        if run in C.pos_correct[np.where(C.pos_correct==sbj),:]:
                            print("\nCorrecting pos-file for run %s!\n" % run)
                            head_pos[0,1:] = head_pos[1,1:] # replace first row

                else:

                    head_pos = None


                raw_out = mne.preprocessing.maxwell_filter(raw, calibration=C.MF['cal'],
                                                       cross_talk=C.MF['ctc'],
                                                       st_duration=st_duration,
                                                       origin=origin,
                                                       destination=destination,
                                                       int_order=C.MF['in'],
                                                       ext_order=C.MF['out'],
                                                       st_correlation=C.MF['st_correlation'],
                                                       coord_frame=C.MF['frame'],
                                                       regularize=C.MF['regularize'],
                                                       head_pos=head_pos)
                

                raw_fname_out, log_fname_out = C.fname_raw_out(C, subject, run, st_duration, origin)

                raw_out.save(raw_fname_out, overwrite=True)

    # done
"""
=========================================================
BEM Model and Source Space
=========================================================

"""
# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

print __doc__

# Russell's addition
import os.path as op
import sys
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/freesurfer/6.0.0/')

import importlib

#
#sys.path.append('/imaging/local/software/python_packages/nibabel/2.0.0')
#sys.path.append('/imaging/local/software/python_packages/pysurfer/v0.3.1')
# End

import glob

import mne

## get analysis parameters from config file
if len(sys.argv)>1:
    print sys.argv[1]
    module_name = sys.argv[1]
else:
    module_name = 'WH_config'

C = importlib.import_module(module_name)
reload(C)

# mne.set_log_file(fname=C.bem_log_file, overwrite=True)

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

# where MRIs are
subjects_dir = C.subjects_dir

# Where MEG raw data (and trans-files) are
raw_path_sss = C.raw_path_sss

bem_path = C.bem_path

cov_path = C.cov_path

###
for sbj in subjs:

    subject = 'Sub%02d' % sbj

    print 
    print('Creating inverse operator for %s' % subject)

    for st_duration in C.MF['st_duration']:

        for origin in C.MF['origin']:

            raw_fname, _ = C.fname_raw_out(C, subject, C.MF['ref_sess'], C.fwd_st, C.fwd_origin)

            raw = mne.io.read_raw_fif(raw_fname, preload=False)

            info = raw.info # info from raw data
            
            # covariance matrix (filter with wildcard)            
            cov_fname = C.fname_cov(C, subject, st_duration, origin, C.inv_cov_latwin, C.inv_method, '*')

            # method may be underspecified, since it may be ranked differently for different subjects
            cov_fname = glob.glob(cov_fname)[0] # be careful if multiple options present

            noise_cov = mne.read_cov(cov_fname)

            ### EEG+MEG
            pick_eeg, pick_meg = True, True

            fwd_fname = C.fname_ForwardSolution(C, subject, 'EEGMEG')

            inv_fname = C.fname_InverseOperator(C, subject, st_duration, origin, C.inv_cov_latwin, 'EEGMEG')

            fwd = mne.read_forward_solution(fwd_fname, surf_ori=True)

            fwd = mne.pick_types_forward(fwd, meg=pick_meg, eeg=pick_eeg)

            # make an inverse operator    
            inverse_operator = mne.minimum_norm.make_inverse_operator(info, fwd, noise_cov, loose=0.2, depth=None, verbose=None)
            
            mne.minimum_norm.write_inverse_operator(inv_fname, inverse_operator)

            ### EEG only
            pick_eeg, pick_meg = True, False

            fwd_fname = C.fname_ForwardSolution(C, subject, 'EEGMEG')

            inv_fname = C.fname_InverseOperator(C, subject, st_duration, origin, C.inv_cov_latwin, 'EEG')

            fwd = mne.read_forward_solution(fwd_fname, surf_ori=True)

            fwd = mne.pick_types_forward(fwd, meg=pick_meg, eeg=pick_eeg)

            # make an inverse operator    
            inverse_operator = mne.minimum_norm.make_inverse_operator(info, fwd, noise_cov, loose=0.2, depth=None, verbose=None)
            
            mne.minimum_norm.write_inverse_operator(inv_fname, inverse_operator)

            ### MEG only
            pick_eeg, pick_meg = False, True

            fwd_fname = C.fname_ForwardSolution(C, subject, 'MEG')

            inv_fname = C.fname_InverseOperator(C, subject, st_duration, origin, C.inv_cov_latwin, 'MEG')

            fwd = mne.read_forward_solution(fwd_fname, surf_ori=True)

            fwd = mne.pick_types_forward(fwd, meg=pick_meg, eeg=pick_eeg)

            # make an inverse operator    
            inverse_operator = mne.minimum_norm.make_inverse_operator(info, fwd, noise_cov, loose=0.2, depth=None, verbose=None)
            
            mne.minimum_norm.write_inverse_operator(inv_fname, inverse_operator)

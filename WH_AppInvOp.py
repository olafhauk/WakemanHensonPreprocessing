"""
=========================================================
Apply Inverse Operator to evoked data
=========================================================

"""
# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

print __doc__

# Russell's addition
import os
import os.path as op
import sys
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/freesurfer/6.0.0/')

import importlib

# import matplotlib
# matplotlib.use('Agg') # possibly for running on cluster
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

###
for sbj in subjs:

    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.stc_path, subject)
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    for st_duration in C.MF['st_duration']:

        for origin in C.MF['origin']:

            evo_fname = C.fname_evo(C, subject, st_duration, origin)

            evokeds = mne.read_evokeds(evo_fname)

            for modality in C.inv_modalities: # EEG/MEG/EEGMEG

                inv_fname = C.fname_InverseOperator(C, subject, st_duration, origin, C.inv_cov_latwin, modality)

                print('Reading Inverse Operator from %s.' % inv_fname)

                inverse_operator = mne.minimum_norm.read_inverse_operator(inv_fname)
                
                lambda2 = 1.0 / C.snr ** 2

                for evo in evokeds:

                    stc = mne.minimum_norm.apply_inverse(evo, inverse_operator, lambda2, C.stc_method,
                                                                    pick_ori=None)

                    stc_fname = C.fname_STC(C, subject, st_duration, origin, C.inv_cov_latwin, modality,
                                                                                            evo.comment)

                    print('Writing STC to: %s' % stc_fname)

                    stc.save(stc_fname)


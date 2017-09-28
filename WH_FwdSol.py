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

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster
#sys.path.append('/imaging/local/software/python_packages/nibabel/2.0.0')
#sys.path.append('/imaging/local/software/python_packages/pysurfer/v0.3.1')
# End

import mne
# mne.set_log_file(fname='/group/erp/data/olaf.hauk/MEG/Plausibility_EyeTracking/MRI/BEM_ForwardSolution.log', overwrite=None)

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

trans_path = C.trans_path

for sbj in subjs:
    subject = 'Sub%02d' % sbj

    print 
    print("###\nCreating forward solution for %s\n###" % subject)

    raw_fname, _ = C.fname_raw_out(C, subject, C.MF['ref_sess'], C.fwd_st, C.fwd_origin)

    print('Info from %s' % raw_fname)

    # MRI-MEG co-registration transformation
    fname_trans, _ = C.fname_MF_trans(C, subject, C.MF['ref_sess'])

    print('Transformation from %s' % fname_trans)
   
    src_fname = C.fname_src_space(C, subject)
    print('Source space from %s' % src_fname)

    src = mne.read_source_spaces(src_fname)

    ### one-shell BEM for MEG
    bem_fname = C.fname_BEM(C, subject, 'MEG')
    
    print('Reading BEM from %s.' % bem_fname)

    bem = mne.bem.read_bem_solution(bem_fname)
    
    fwd_fname = C.fname_ForwardSolution(C, subject, 'MEG')

    print('Forward MEG: %s' % fwd_fname)

    fwd = mne.make_forward_solution(raw_fname, trans=fname_trans, src=src, bem=bem,
                                    meg=True, eeg=False, mindist=5.0)

    mne.write_forward_solution(fwd_fname, fwd, overwrite=True)

    ### three-shell BEM for MEG
    bem_fname = C.fname_BEM(C, subject, 'EEGMEG')

    print('Reading BEM from %s.' % bem_fname)

    bem = mne.bem.read_bem_solution(bem_fname)
    
    fwd_fname = C.fname_ForwardSolution(C, subject, 'EEGMEG')

    print('Forward EEGMEG: %s' % fwd_fname)

    fwd = mne.make_forward_solution(raw_fname, trans=fname_trans, src=src, bem=bem,
                                    meg=True, eeg=True, mindist=5.0)

    mne.write_forward_solution(fwd_fname, fwd, overwrite=True)

    print(fwd)

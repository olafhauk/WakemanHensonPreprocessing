"""
=========================================================
BEM Model and Source Space
=========================================================

"""
# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

print __doc__

import os.path as op
import sys

# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/mne_python/v0.15/')
sys.path.insert(1, '/imaging/local/software/freesurfer/6.0.0/')

import importlib

import matplotlib
matplotlib.use('Agg') # possibly for running on cluster

execfile("/imaging/local/software/mne_python/set_MNE_2.7.3_FS_6.0.0_environ.py")

#sys.path.append('/imaging/local/software/python_packages/nibabel/2.0.0')
#sys.path.append('/imaging/local/software/python_packages/pysurfer/v0.3.1')
# End

# Failed attempt to send output to both a file and stderr
import logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

import mne

## get analysis parameters from config file
if len(sys.argv)>1:
    print sys.argv[1]
    module_name = sys.argv[1]
else:
    module_name = 'WH_config'

C = importlib.import_module(module_name)
reload(C)

mne.set_log_file(fname=C.bem_log_file, overwrite=False)

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

subjects_dir = C.subjects_dir

conductivity_1 = C.bem_conductivity_1  # for single layer
conductivity_3 = C.bem_conductivity_3  # for three layers

for sbj in subjs:
    subject = 'Sub%02d' % sbj

    sub_dir = op.join(C.bem_path, subject, 'bem')
    if not op.exists(sub_dir):
        os.mkdir(sub_dir)

    print "###\nMaking BEM model for " + subject + "\n###"

    ### one-shell BEM for MEG
    model = mne.make_bem_model(subject=subject, ico=C.bem_ico,
                                conductivity=conductivity_1,
                                subjects_dir=subjects_dir)
    
    bem = mne.make_bem_solution(model)

    bem_fname = op.join(C.bem_path, subject, 'bem', subject + '_MEG-bem.fif')

    print "###\nWriting BEM solution to " + bem_fname + "\n###"
    mne.bem.write_bem_solution(bem_fname, bem)

    ### three-shell BEM for EEG+MEG
    model = mne.make_bem_model(subject=subject, ico=C.bem_ico,
                                conductivity=conductivity_3,
                                subjects_dir=subjects_dir)
    bem = mne.make_bem_solution(model)

    bem_fname = op.join(C.bem_path, subject, 'bem', subject + '_EEGMEG-bem.fif')

    print "###\nWriting BEM solution to " + bem_fname + "\n###"
    mne.bem.write_bem_solution(bem_fname, bem)
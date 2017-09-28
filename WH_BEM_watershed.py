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

# don't do make_watershed_bem with these, because their inner skulls had to be shrunk
# use WH_watershed_shrink_3mm.sh instead
shrink_subs = ['Sub04', 'Sub05', 'Sub08']

for sbj in subjs:
    subject = 'Sub%02d' % sbj

    # check if watershed to be applied    
    if subject in shrink_subs:
        print('Shrinking skull for %s' % subject)
        os_cmd = '/home/olaf/MEG/WakemanHensonEMEG/WH_shrink_innerskull.sh %s' % subject
        os.system(os_cmd)
    else:
        print('MNE watershed for %s' % subject)

        mne.bem.make_watershed_bem(subject, subjects_dir=subjects_dir, atlas=True,
                                overwrite=True)
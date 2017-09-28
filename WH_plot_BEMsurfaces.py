"""
=========================================================
Test script to compute  evoked data
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


### Function that plots BEM surfaces for one orientation
def plot_one_bem(subject, orientation, fig_dir):
    fig_bem = mne.viz.plot_bem(subject=subject, subjects_dir=C.subjects_dir, orientation=orientation, show=False)
    
    fig_fname = op.join(fig_dir, subject + '_' + orientation + '.pdf')
    print "Writing " + fig_fname
    fig_bem.savefig(fig_fname)

    return fig_bem


### Plot BEM surfaces one by one
orientations = ['coronal', 'axial', 'sagittal']

for [si,sbj] in enumerate(subjs):
    
    subject = 'Sub%02d' % sbj

    [plot_one_bem(subject, orientation, C.bem_fig_dir) for orientation in orientations]
    




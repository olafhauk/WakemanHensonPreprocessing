"""
=========================================================
Visualise Source Space
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

import numpy as np  # noqa
from mayavi import mlab  # noqa
from surfer import Brain  # noqa

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


for [si,sbj] in enumerate(subjs):
    
    subject = 'Sub%02d' % sbj

    src_fname = op.join(C.bem_path, subject, subject + '_' + C.src_spacing + '-src.fif')

    src = mne.read_source_spaces(src_fname)

    brain = Brain(subject, 'lh', 'inflated', subjects_dir=subjects_dir)
    
    surf = brain._geo

    vertidx = np.where(src[0]['inuse'])[0]

    mlab.points3d(surf.x[vertidx], surf.y[vertidx],
                  surf.z[vertidx], color=(1, 1, 0), scale_factor=1.5)

    fig_fname = op.join(fig_dir, subject + '_' + C.src_spacing + '-src.fif')

    mlab.savefig(fig_fname, figure=mlab.gcf())
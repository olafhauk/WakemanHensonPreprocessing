"""
=========================================================
Visualise MEG-MRI coordinate transformation
run in mne_python_glx, requires mayavi
=========================================================

"""
# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

# NOTE: Don't know how to suppress figures popping up

print __doc__

import os.path as op
import sys

# for qsub: check matplotlib.use('Agg'), plt.ion(), plt.show(), do_show
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/envs/mayavi_env/lib/python2.7/site-packages')
sys.path.insert(1, '/imaging/local/software/mne_python/v0.15/')
sys.path.insert(1, '/imaging/local/software/freesurfer/6.0.0/')

import importlib

import mayavi
from mayavi import mlab

import mne

execfile("/imaging/local/software/mne_python/set_MNE_2.7.3_FS_6.0.0_environ.py")

#sys.path.append('/imaging/local/software/python_packages/nibabel/2.0.0')
#sys.path.append('/imaging/local/software/python_packages/pysurfer/v0.3.1')
# End

# Failed attempt to send output to both a file and stderr
import logging
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

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


def plot_one_trans(info, subject):
    
    src_fname = C.fname_src_space(C, subject)

    src = mne.read_source_spaces(src_fname)

    trans_fname, _ = C.fname_MF_trans(C, subject, '')

    mayavi.engine.current_scene.scene.off_screen_rendering = True
    
    fig_trans = mne.viz.plot_trans(info, trans_fname, subjects_dir=C.subjects_dir, subject=subject,
                                    dig=True, meg_sensors=True, eeg_sensors='original', src=src)

    _, fig_fname = C.fname_MF_trans(C, sbj, 'front')
    print "Writing " + fig_fname
    fig_trans.scene.save(fig_fname)
    
    fig_trans.scene.x_minus_view() # left view
    _, fig_fname = C.fname_MF_trans(C, sbj, 'left')
    fig_trans.scene.save(fig_fname)

    fig_trans.scene.x_plus_view() # right view
    _, fig_fname = C.fname_MF_trans(C, sbj, 'right')
    fig_trans.scene.save(fig_fname)

    return fig_trans


for [si,sbj] in enumerate(subjs):
    
    subject = 'Sub%02d' % sbj

    if not op.exists(C.coor_fig_dir):
        os.mkdir(C.coor_fig_dir)

    raw_fname, _ = C.fname_raw_out(C, subject, C.ref_sess, C.fwd_st, C.fwd_origin)

    info = mne.io.read_info(raw_fname)

    plot_one_trans(info, subject)

print('\nType: from mayavi imort mlab | mlab.close(all=True) when you are ready')
### !/imaging/local/software/miniconda/envs/mne0.20/bin/python
"""
=========================================================
Plot whole-brain resolution metrics for WH dataset.
run RA_plot_metrics.py RA_config
=========================================================

"""
# OH, May 2019

print(__doc__)

import sys

import os
from os import stat  # to get file sizes

import glob

import numpy as np

from mayavi import mlab
mlab.options.offscreen = True

# needed to run on SLURM
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from os import path as op
import importlib

from time import sleep  # to add delay while saving figures

import mne

print('MNE Version: %s\n\n' % mne.__version__)  # just in case

# os.environ["MNE_ROOT"] = "/imaging/local/software/mne/mne_2.7.3/x86_64/MNE-2.7.3-3268-Linux-x86_64/"
# os.environ["SUBJECTS_DIR"] = "/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI/"

module_name = sys.argv[1]
C = importlib.import_module(module_name)
# importlib.reload(C)

inpath = op.join(C.resolution_path, C.resolution_subdir, 'fsaverage')

# it should exist, but...
if not op.exists(C.figures_dir):
    os.mkdir(C.figures_dir)

# list of parameters settings to apply

# the following will be iterated per item in paramlist
functions = ['psf', 'ctf']  # type of resolution functions
metrics = ['peak_err', 'sd_ext', 'peak_amp', 'sum_amp']  # type of resolution metrics

# 'paramlist' can contain parameter combinations that are not necessarily
# nested.

# inverse methods and contrasts to average
# (method/contrast, max scaling for (err, ext, amp))

# All
methods = [('MNE', (5., 5., 1.)),
           ('MNE_dep80', (5., 5., 1.)),
           ('sLOR', (5., 5., 1.)),
           ('dSPM', (5., 5., 1.)),
           ('eLOR', (5., 5., 1.)),
           ('LCMV_-200_0ms', (5., 5., 1.)),
           ('LCMV_50_250ms', (5., 5., 1.)),
           (('MNE', 'MNE_dep80'), (5., 1., .5)),
           (('MNE', 'dSPM'), (5., 1., .5)),
           (('MNE', 'sLOR'), (5., 1., .5)),
           (('MNE', 'eLOR'), (5., 1., .5)),
           (('sLOR', 'eLOR'), (5., 1., .5)),
           (('dSPM', 'sLOR'), (5., 1., .5)),
           (('MNE', 'LCMV_-200_0ms'), (5., 5., .5)),
           (('MNE', 'LCMV_50_250ms'), (5., 5., .5)),
           (('LCMV_-200_0ms', 'LCMV_50_250ms'), (5., 1., .5))]

# # LCMV only
# methods = [('LCMV_-200_0ms', (5., 10., 1.)),
#            ('LCMV_50_250ms', (5., 10., 1.)),
#            (('MNE', 'LCMV_-200_0ms'), (2., 5., .5)),
#            (('MNE', 'LCMV_50_250ms'), (2., 5., .5)),
#            (('LCMV_-200_0ms', 'LCMV_50_250ms'), (2., 5., .5))]

paramlist = [
    dict(functions=functions, metrics=metrics, methods=methods,
         chtype='eegmeg', snr=3., loose=0., depth=0.)
]

# for filenames, remove in future
st_duration = C.res_st_duration
origin = C.res_origin

subject = 'fsaverage'

for params in paramlist:

        # paramters for resolution matrix and metrics
        functions = params['functions']
        metrics = params['metrics']
        methods = params['methods']
        chtype = params['chtype']
        snr = params['snr']
        loose = params['loose']
        depth = params['depth']

        lambda2 = 1. / snr ** 2

        # methods and thresholds for plotting
        for (method, threshs) in methods:  # which methods to subtract

            if type(method) == tuple:  # if contrast specified

                method_str = '%s-%s' % (method[0], method[1])

            else:  # if just one method specified

                method_str = method

            for function in functions:

                for metric in metrics:

                    # for filenames
                    lamb2_str = str(lambda2).replace('.', '')
                    if len(lamb2_str) > 3:
                        lamb2_str = lamb2_str[:3]

                        if loose is None:
                            loose = 0
                        loo_str = 'loo%s' % str(int(100 * loose))

                        if depth is None:
                            depth = 0
                        dep_str = 'dep%s' % str(int(100 * depth))

                    stctext = '%s_%s_%s_mph' % (function, metric, method_str)

                    # select appropriate threshold for plotting
                    if 'err' in metric:
                            thresh = threshs[0]
                    elif 'ext' in metric:
                        thresh = threshs[1]
                    elif 'amp' in metric:
                        thresh = threshs[2]
                    else:
                        print('Not recognised this metric %s.' % metric)

                    fname_mph = C.fname_STC(C, C.resolution_subdir, subject,
                                            stctext)

                    # READ EXISTING SOURCE ESTIMATE
                    print('Reading: %s.' % fname_mph)
                    stc = mne.read_source_estimate(fname_mph, subject)

                    # time_label = '%s %s %s' % (method, function, metric)
                    time_label = ''  # easier for paper figures

                    # continue until figure output has decent size,
                    # i.e. it didn't fail
                    st_size = 0

                    max_size = 10000  # bytes

                    max_tries = 3  # try 3 times

                    tries = 1

                    while st_size < max_size and tries <= max_tries:

                        if tries > 1:

                            print('Trying again (%d).' % tries)

                        print('Plotting.')
                        brain = stc.plot(
                            time_label=time_label, subjects_dir=C.subjects_dir,
                            subject='fsaverage', colorbar=False,
                            clim=dict(kind='value',
                                      pos_lims=[0, thresh / 2., thresh]))

                        fig_fname = op.join(C.figures_dir, stctext + '.jpg')

                        print('Saving.')

                        print('Saving figure to %s.' % fig_fname)

                        mlab.savefig(fig_fname)

                        st_size = stat(fig_fname).st_size

                        print('Size: %d' % st_size)

                        tries = tries + 1

                        mlab.close(all=True)

                    if tries == 4:

                        print('###\nFigure not plotted correctly!\n###')

            # average individual PSFs and CTFs
            if type(method) is not tuple:  # if no subtraction

                # read data covariance matrix for LCMV beamformer
                # covariance matrix (filter with wildcard)
                filetext = '%s_PSF*mph-lh.stc' % (method)
                fname_stc = C.fname_STC(
                    C, C.resolution_subdir, subject, filetext)

                # get list of matching filenames for PSFs
                fname_stcs = glob.glob(fname_stc)  # be careful if multiple options present

                # now append filenames for CTFs
                filetext = '%s_CTF*mph-lh.stc' % (method)
                fname_stc = C.fname_STC(
                    C, C.resolution_subdir, subject, filetext)

                # add list items to existing file list
                fname_stcs += glob.glob(fname_stc)

                for [fi, ff] in enumerate(fname_stcs):

                    # READ EXISTING SOURCE ESTIMATE
                    print('Reading: %s.' % ff)
                    stc = mne.read_source_estimate(ff, subject)

                    # treshold for colourbar
                    thresh = np.abs(stc.data).max()

                    # time_label = '%s %s %s' % (method, function, metric)
                    time_label = ''  # easier for paper figures

                    # continue until figure output has decent size,
                    # i.e. it didn't fail
                    st_size = 0

                    max_size = 10000  # bytes

                    max_tries = 3  # try 3 times

                    tries = 1

                    while st_size < max_size and tries <= max_tries:

                        if tries > 1:

                            print('Trying again (%d).' % tries)

                        print('Plotting.')
                        brain = stc.plot(
                            time_label=time_label, subjects_dir=C.subjects_dir,
                            subject='fsaverage', colorbar=False,
                            clim=dict(kind='value',
                                      pos_lims=[0, thresh / 2., thresh]))

                        stctext = ff.split('/')[-1][:-7] + '.jpg'

                        fig_fname = op.join(C.figures_dir, stctext)

                        print('Saving figure to %s.' % fig_fname)

                        mlab.savefig(fig_fname)

                        st_size = stat(fig_fname).st_size

                        print('Size: %d' % st_size)

                        tries = tries + 1

                        mlab.close(all=True)

                    if tries == 4:

                        print('###\nFigure not plotted correctly!\n###')

#!/imaging/local/software/anaconda/latest/x86_64/bin/python
"""
==========================================
Maxfilter Wakeman&Henson data using Neuromag MF
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
    

    for run in sess:

        raw_fname_in = C.fname_raw_in(C, subject, run)

        # Hackish way of reading bad channels from the log.
        log_fname = op.join(raw_path_in, subject, 'MEEG', 'MaxFilterOutput', 'run_%.2d_sss_log.txt' % run)
        bads = []
        with open(log_fname) as fid:
            for line in fid:
                if line.startswith('Static bad channels'):
                    chs = line.split(':')[-1].split()
                    bads = ['%04d' % int(ch) for ch in chs]
                    break

                    
            print("BAD CHANNELS:\n")
            print(bads)

        if bads == []:
            bad_str = ''
        else:
            bad_str = '-bad ' + ' '.join(x for x in bads)

        ## MAXFILTER
        for st_duration in C.MF['st_duration']:

            # file part for type of maxfilter
            # replace period to avoid confusion with file names
            if st_duration == None:
                st_cmd = ''
            else:
                st_cmd = ' -st %s ' % str(int(st_duration))

            for origin in C.MF['origin']:                

                ori_cmd = ' -origin %.0f %.0f %.0f ' % (1000*origin[0], 1000*origin[1], 1000*origin[2])

                raw_fname_out, log_fname_out = C.fname_raw_out(C, subject, run, st_duration, origin)

                order_cmd = '-in %d  -out %d' % (C.MF['in'], C.MF['out'])

                if not(C.MF['mv']==''):
                    mv_cmd = '-movecomp %s' % C.MF['mv']

                mf_cmd = '  %s \
                            -f %s \
                            -o %s \
                            -trans %s \
                            -corr %f \
                            -frame %s \
                            -regularize %s \
                            %s \
                            %s \
                            %s \
                            %s \
                            %s \
                            -autobad off \
                            -force \
                            -linefreq 50 \
                            -v \
                            | tee %s' \
                            % ( C.MF['NM_cmd'], 
                                raw_fname_in,
                                raw_fname_out,
                                raw_fname_ref,
                                C.MF['st_correlation'],
                                C.MF['frame'],
                                C.MF['regularize'],
                                bad_str,
                                st_cmd,
                                ori_cmd,
                                order_cmd,
                                mv_cmd,
                                log_fname_out)

                print('Maxfilter command: %s' % mf_cmd)
                
                os.system(mf_cmd)
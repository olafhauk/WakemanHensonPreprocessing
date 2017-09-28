###
# copy Wakeman/Henson (only EMEG data), e.g. for head transformation
###

import os
from shutil import copy

# path to data set
data_path = '/imaging/rh01/Methods/DanData/Raw/'

# where data will be copied to
out_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/RAW/'

# subject numbers (from Roni's Matlab script)
subjs  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# subjs = [7]

# sessions per subject
sess = [1, 2, 3, 4, 5, 6]


for [si,sbj] in enumerate(subjs):
    sbj_path = "/Sub" + "%.2d" % sbj

    cp_path = out_path + sbj_path

    # make subject sub-directory if necessary
    if not os.path.exists(cp_path):
    	os.makedirs(cp_path)

    for ses in sess:

        ## read and modify raw data

        raw_fname = data_path + sbj_path + "/MEEG/run_" + "%.2d" % ses + "_sss.fif"

        print "Copying %s" + raw_fname

        copy(raw_fname, cp_path)


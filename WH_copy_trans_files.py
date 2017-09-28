###
# copy trans-files from RAW into separate directories
# to protect from accidental deletion
###

import sys
import os.path as op
from shutil import copy

import importlib

## get analysis parameters from config file
if len(sys.argv)>1:
    print sys.argv[1]
    module_name = sys.argv[1]
else:
    module_name = 'WH_config'

C = importlib.import_module(module_name)
reload(C)

# where Clare's trans-files are
raw_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/RAW/'

for [si,sbj] in enumerate(C.subjs):

    subject = "Sub%0.2d" % sbj
    
    from_file = op.join(raw_path, subject, 'run_04_sss-trans.fif')

    to_file = op.join(C.trans_path, subject + '_' + 'run_04_sss-trans.fif')
    
    print "Copying %s to %s" % (from_file, to_file)

    copy(from_file, to_file)


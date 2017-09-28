"""
=======================================
Config file for Wakeman&Henson data set
=======================================

place it in same folder as py-files
"""

##########################################################
## SYSTEM variables
##########################################################

import sys
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/sklearn/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/pysurfer/')
sys.path.insert(1, '/imaging/local/software/anaconda/2.4.1/2/lib/python2.7/site-packages/nibabel/')

##########################################################
## GENERAL
##########################################################

# path to unmaxfiltered raw data
raw_path_in = '/imaging/rh01/Methods/DanData/RawFIF/'

# output path for maxfiltered raw data
raw_path_sss = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/RAW'

# path to MRI/MEG transformations
trans_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/TRANS'

# raw_path_sss = '/imaging/rh01/Methods/DanData/Raw'

# subject numbers (from Roni's Matlab script)
subjs  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# sessions per subject
sess = [1, 2, 3, 4, 5, 6]
# sess = [1, 2]

# reference session for trans option
ref_sess = 3

##########################################################
## MAXFILTER
##########################################################

# maxfilter parameters
# problems with SVD converge in MF when doing more than 2 options at once
# (probably due to memory problems)
MF = {# 'NM_cmd': '/imaging/local/software/neuromag/bin/util/x86_64-pc-linux-gnu/maxfilter-2.2',
     'NM_cmd': '/imaging/local/software/neuromag/bin/util/maxfilter-2.2.12',
     'cal': '/neuro/databases/sss/sss_cal.dat',
     'ctc': '/neuro/databases/ctc/ct_sparse.fif',
     # 'st_duration': [None,10.], # list
     'st_duration': [None,10.], # list          
     # 'origin': [(0., 0., 0.03),(0., 0., 0.04),(0., 0., 0.05)], # list
     'origin': [(0., 0., 0.035),(0., 0., 0.045),(0., 0., 0.055)], # list            
     'ref_sess': 3,
     'st_correlation': 0.98,
     'in': 8,
     'out': 3,
     'regularize': 'in',
     'frame': 'head',
     'mv': 'inter'}

st_string_stem = 'ST'
ori_string_stem = 'O'

# only for use of post-MF processing
# different py-scripts for MNE/NM maxfilter options
MF_method = '_MN' # '_NM'

##########################################################
### EPOCHING
##########################################################

# path to epoched data
epo_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/EPO/'

# path for pre-processing figures
fig_pre_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/Figures/'

# path for MNE-defined events
eve_mne_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/EVE/'

event_id=[5,6,7,13,14,15,17,18,19]

# epoch start/end latencies (s)
epo_t1, epo_t2 = -0.2, 0.4

# baseline
epo_baseline = (epo_t1, 0.)

# bandpass filter (Butterworth 4-th order)
h_freq = 40. # Hz
l_freq = 0.1

# artefact rejection thresholds
reject = dict(grad=4000e-13, mag=4e-12, eog=180e-6)

##########################################################
### AVERAGING
##########################################################

# path to evoked responses
evo_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/AVG/'

##########################################################
### COVARIANCE
##########################################################

cov_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/COV/'

cov_tmin = -0.2
cov_tmax = 0.

cov_methods = ['auto'] # list of lists if best covmat to be chosen
# cov_methods = [['empirical', 'shrunk']] # list


##########################################################
### SOURCE SPACE
##########################################################

# where MRIs are
subjects_dir = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI/'

src_spacing = 'oct6'

##########################################################
### BEM
##########################################################

# where BEM figures will be written to
bem_path = subjects_dir # will be in subject/bem

bem_log_file = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI/BEMs/BEM_Model_and_SourceSpace.log'

bem_fig_dir = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/Figures/BEM_plot'

coor_fig_dir = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/Figures/CoorTrans_plot'

bem_ico = 4

bem_conductivity_1 = (0.3,)  # for single layer
bem_conductivity_3 = (0.3, 0.006, 0.3)  # for three layers


##########################################################
### FORWARD AND INVERSE OPERATORS
##########################################################

# for info and covariance matrices
mod_st_string = 'ST0'
mod_ori_string = 'O50'

# for inverse operator
inv_lat_str = '-200_400ms'
inv_cov_str = 'cov-200_0'
inv_method = 'empirical' # used for file filter, number of method name


##########################################################
### APPLY INVERSE OPERATOR TO EVOKED DATA
##########################################################

stc_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/STC/'
stc_method = 'MNE'
snr = 3.
invops = ['EEGMEG', 'MEG', 'EEG'] # which invop files to apply
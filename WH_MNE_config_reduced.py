"""
=======================================
Config file for Wakeman&Henson data set
MNE-Maxfiltered data
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

import os.path as op

import numpy as np

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
ref_sess = 4

# stimulus presentation delay wrt trigger (e.g. projector) (s)
delay = 0.0345

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
     'st_duration': [10], # list
     # 'st_duration': [None,10.], # list          
     'origin': [(0., 0., 0.045)], # list
     # 'origin': [(0., 0., 0.035),(0., 0., 0.045),(0., 0., 0.055)], # list            
     'ref_sess': 4,
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

# for this subject,run, the first line of the pos-file seems wrong
# note: subject number (start at 1), not index
pos_correct = np.array([[13,4]]) # list of lists

##########################################################
### EPOCHING
##########################################################

# path to epoched data
epo_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/EPO/'

# path for pre-processing figures
fig_pre_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/Figures/'

# path for MNE-defined events
eve_mne_path = '/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/data/EVE/'

event_id = {
    'fc/fm/fi': 5, # face/familiar/first
    'fc/fm/im': 6, # /immediate
    'fc/fm/lo': 7, # /long
    'fc/uf/fi': 13, # /unfamiliar
    'fc/uf/im': 14,
    'fc/uf/lo': 15,
    'sc/fi': 17, # scrambled/
    'sc/im': 18,
    'sc/lo': 19,
}

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

# cov_methods = ['auto'] # list of lists if best covmat to be chosen
cov_methods = [['empirical', 'shrunk', 'factor_analysis']] # list


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

# for use in forward solution
fwd_st = None
fwd_origin = (0.,0.,0.045)

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
inv_modalities = ['EEGMEG', 'MEG', 'EEG'] # which invop files to apply


###########################################################
# FUNCTIONS FOR FILENAMES
###########################################################

def fname_raw_in(C, subject, run):

     subject = str(subject)
     raw_fname_in = op.join(C.raw_path_in, subject, 'MEEG', 'run_%.2d_raw.fif' % run)

     return raw_fname_in

def fname_raw_out(C, subject, run, st_duration, origin):

     subject = str(subject)

     # file part for type of maxfilter
     # replace period to avoid confusion with file names
     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     raw_fname_out = op.join(C.raw_path_sss, subject, 'run_%.2d' % run +
                                          '_' + st_string + '_' + ori_string + C.MF_method + '_raw.fif')

     log_fname_out = op.join(raw_path_sss, subject, 'run_%.2d' % run +
                              '_' + st_string + '_' + ori_string + C.MF_method + '_raw.txt')

     return raw_fname_out, log_fname_out


def fname_MF_pos(C, subject, run):

     subject = str(subject)

     pos_fname = op.join(raw_path_sss, subject, 'run_%.2d' % run + '_raw.pos')

     return pos_fname


def fname_trans(C, subject, run):

     subject = str(subject)

     trans_fname = op.join(C.trans_path, subject + '_run_%.2d' % run + '_sss-trans.fif')

     return trans_fname


def fname_eve(C, subject, run, st_duration, origin):

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     fig_fname = op.join(C.fig_pre_path, subject + '_run_%.2d' % run + '_' + st_string + '_' + 
                                                       ori_string + C.MF_method + '_eve.pdf')

     # file name to which to write event info
     eve_fname = op.join(C.eve_mne_path, subject + '_run_%.2d' % run +
                    '_' + st_string + '_' + ori_string + C.MF_method + '-eve.fif')

     return eve_fname, fig_fname



def fname_epo(C, subject, st_duration, origin):

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     # identify epoch latencies in filename (no ".")
     lat_tmp = str(int(1000*C.epo_t1)) + '_' + str(int(1000*C.epo_t2)) + "ms"
     lat_str = lat_tmp.replace(".", "")

     # identify filter in filename (no ".")
     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")

     epo_fname = op.join(C.epo_path, subject, subject + '_' + st_string + '_' + ori_string + C.MF_method + 
                                    '_' + lat_str + "_" + filt_str + "-epo.fif")

     return epo_fname


def fname_cov(C, subject, st_duration, origin, method, cov_i):

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     # identify epoch latencies in filename (no ".")
     lat_tmp = str(int(1000*C.epo_t1)) + '_' + str(int(1000*C.epo_t2)) + "ms"
     lat_str = lat_tmp.replace(".", "")

     # identify filter in filename (no ".")
     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")

     tmin_str = str(int(1000*C.cov_tmin)) # time interval as string in ms
     tmax_str = str(int(1000*C.cov_tmax))
     cov_str = 'cov' + tmin_str + '_' + tmax_str

     method_now = method + str(cov_i) # add the ranking of covmat

     cov_fname = op.join(C.cov_path, subject, subject + '_' + st_string + '_' + ori_string + 
                                        C.MF_method + '_' + lat_str + "_" + filt_str + '_' + cov_str + '_'
                                        + method_now + "-cov.fif")

     return cov_fname


def fname_evo(C, subject, st_duration, origin):

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     # identify epoch latencies in filename (no ".")
     lat_tmp = str(int(1000*C.epo_t1)) + '_' + str(int(1000*C.epo_t2)) + "ms"
     lat_str = lat_tmp.replace(".", "")

     # identify filter in filename (no ".")
     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")

     evo_fname = op.join(C.evo_path, subject, subject + '_' + st_string + '_' + ori_string + 
                                            C.MF_method + '_' + lat_str + '_' + filt_str + '-ave.fif')

     return evo_fname


def fname_fig_evo(C, subject, st_duration, origin, chan_type, cond):

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     # identify epoch latencies in filename (no ".")
     lat_tmp = str(int(1000*C.epo_t1)) + '_' + str(int(1000*C.epo_t2)) + "ms"
     lat_str = lat_tmp.replace(".", "")

     # identify filter in filename (no ".")
     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")


     fig_fname_curves = op.join(C.evo_path, subject, subject + '_' + st_string + '_' + ori_string + 
                                            C.MF_method + '_' + lat_str + '_' + filt_str + '_' + cond +
                                            '_ave.pdf')

     fig_fname_topo = op.join(C.evo_path, subject, subject + '_' + st_string + '_' + ori_string + 
                                            C.MF_method + '_' + lat_str + '_' + filt_str + '_topo_' + 
                                                        cond + '_' + chan_type + '.pdf')

     return fig_fname_curves, fig_fname_topo


def fname_src_space(C, subject):

     subject = str(subject)

     src_fname = op.join(C.bem_path, subject, 'bem', subject + '_' + C.src_spacing + '-src.fif')

     return src_fname


def fname_BEM(C, subject, modality):
     # modality: e.g. EEG, MEG or EEGMEG

     subject = str(subject)

     bem_fname = op.join(C.bem_path, subject, 'bem', subject + '_' + modality + '-bem.fif')

     return bem_fname


def fname_ForwardSolution(C, subject, modality):
     # modality: e.g. EEG, MEG or EEGMEG

     subject = str(subject)

     fwd_fname = op.join(C.evo_path, subject, subject + '_' + modality + '-fwd.fif')

     return fwd_fname


def fname_InverseOperator(C, subject, st_duration, origin, modality):
     # modality: e.g. EEG, MEG or EEGMEG

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")

     inv_fname = op.join(C.evo_path, subject, subject + '_' + st_string + '_' + ori_string + C.MF_method + 
                                                '_' + C.inv_lat_str + '_' + filt_str + '_' + C.inv_cov_str +
                                                '_' + C.inv_method + '_' + modality + '-inv.fif')

     return inv_fname


def fname_STC(C, subject, st_duration, origin, modality, cond):
     # modality: e.g. EEG, MEG or EEGMEG

     subject = str(subject)

     if st_duration == None:
          st_string = C.st_string_stem + '0'
     else:
          st_string = C.st_string_stem + str(st_duration).replace(".", "-")

     # for file name only use z-component in mm
     ori_string = C.ori_string_stem + str(origin[2]*1000).split('.')[0]

     filt_tmp = str(C.l_freq) + '_' + str(C.h_freq) + "Hz"
     filt_str = filt_tmp.replace(".", "")

     stc_fname = op.join(C.stc_path, subject, subject + '_' + st_string + '_' + ori_string + C.MF_method + 
                                                '_' + C.inv_lat_str + '_' + filt_str + '_' + C.inv_cov_str +
                                                '_' + C.inv_method + '_' + modality + '_' + cond)

     return stc_fname

#!/bin/bash
#PBS -q compute
#PBS -l walltime=24:00:00,mem=8GB
#PBS -o /group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI_Freesurfer.err
#PBS -e /group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI_Freesurfer.err

# submit e.g. as qsub -t 0-15 MRI_Freesurfer.sh
# note: indices start at 0

export FSVER='6.0.0'

export FSDIR=${FSROOT}/${FSVER}

export FREESURFER_HOME=/imaging/local/software/freesurfer/${FSVER}/`arch`
export SUBJECTS_DIR=/imaging/`whoami`/subjects
export FUNCTIONALS_DIR=/imaging/`whoami`/sessions
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${FREESURFER_HOME}/lib_flat

echo $FREESURFER_HOME

source $FREESURFER_HOME/FreeSurferEnv.sh

export SUBJECTS_DIR=/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI
echo $SUBJECTS_DIR


subs=(\
'Sub01' \
'Sub02' \
'Sub03' \
'Sub04' \
'Sub05' \
'Sub06' \
'Sub07' \
'Sub08' \
'Sub09' \
'Sub10' \
'Sub11' \
'Sub12' \
'Sub13' \
'Sub14' \
'Sub15' \
'Sub16' \
)

# current subject, as specified in qsub
export sub=${subs[$PBS_ARRAYID]}

echo ${sub}

# convert nifti to mgz, create folders
recon-all -subjid ${sub} -i /imaging/rh01/Methods/DanData/All/${sub}/T1/mprage.nii

# do the lot
recon-all -subjid ${sub} -all
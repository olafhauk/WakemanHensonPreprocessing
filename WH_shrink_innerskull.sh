#!/bin/bash
#PBS -q compute
#PBS -l walltime=12:00:00,mem=64GB
#PBS -o /group/erp/data/olaf.hauk/MEG/Plausibility_EyeTracking/MRI/watershed.out 
#PBS -e /group/erp/data/olaf.hauk/MEG/Plausibility_EyeTracking/MRI/watershed.err

# submit e.g. as: qsub -t 0-2 WH_shrink_innerskull.sh -o ./qsub_out/WH_shrink_innerskull.out -e ./qsub_out/WH_shrink_innerskull.err 
# note: indices start at 0

# note: MNE_watershed_shrink.sh must be in same directory


export FSVER='6.0.0'

export FSDIR=${FSROOT}/${FSVER}

export FREESURFER_HOME=/imaging/local/software/freesurfer/${FSVER}/`arch`
export SUBJECTS_DIR=/imaging/`whoami`/subjects
export FUNCTIONALS_DIR=/imaging/`whoami`/sessions
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${FREESURFER_HOME}/lib_flat

echo $FREESURFER_HOME

source $FREESURFER_HOME/FreeSurferEnv.sh

export MNE_ROOT=/imaging/local/software/mne/mne_2.7.3/x86_64/MNE-2.7.3-3268-Linux-x86_64
export MNE_BIN_PATH=$MNE_ROOT/bin

export PATH=${PATH}:${MNE_BIN_PATH}
# source $MNE_ROOT/bin/mne_setup

export SUBJECTS_DIR=/group/erp/data/olaf.hauk/MEG/WakemanHensonEMEG/MRI/
echo $SUBJECTS_DIR

export SUBJECT=$1
echo $SUBJECT

rm -fR ${SUBJECTS_DIR}/${SUBJECT}/bem/watershed3/*

# decide whether to shrink 2mm or 3mm
/home/olaf/MEG/WakemanHensonEMEG/WH_watershed_shrink_3mm.sh --subject ${SUBJECT} --overwrite

ln -sf ${SUBJECTS_DIR}/${SUBJECT}/bem/watershed3/${SUBJECT}_inner_skull_surface ${SUBJECTS_DIR}/${SUBJECT}/bem/inner_skull.surf

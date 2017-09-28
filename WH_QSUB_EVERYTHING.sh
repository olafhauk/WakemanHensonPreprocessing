#!/bin/bash

# all steps of WH analysis in logical sequence

# WH_QSUB.sh <python script> <config script> <subject indices> <qsub mem> <time delay>

# CHECK
# job chaining: https://www.nics.tennessee.edu/computing-resources/running-jobs/job-chaining

# subjs="0-11,13-15"
# subjs="0-15"
subjs="0-15"

# MNE Maxfilter

# WH_QSUB.sh WH_MF_MNE_pos WH_MNE_config $subjs 128GB

# WH_QSUB.sh WH_MF_MNE WH_MNE_config $subjs 64GB 1200

# WH_QSUB.sh WH_get_eves WH_MNE_config $subjs 4GB 2400

# WH_QSUB.sh WH_epos WH_MNE_config $subjs 16GB

# WH_QSUB.sh WH_covmat WH_MNE_config $subjs 32GB

# WH_QSUB.sh WH_plot_cov WH_MNE_config $subjs 1GB 4000

WH_QSUB.sh WH_evos WH_MNE_config $subjs 2GB

WH_QSUB.sh WH_plot_evocurves WH_MNE_config $subjs 1GB 0030

WH_QSUB.sh WH_plot_topos WH_MNE_config $subjs 1GB 0030


# WH_QSUB.sh WH_FwdSol WH_MNE_config $subjs 2GB

# WH_QSUB.sh WH_InvOp WH_MNE_config $subjs 2GB 0030

# WH_QSUB.sh WH_AppInvOp WH_MNE_config $subjs 1GB 0100


# Neuromag Maxfilter

# WH_QSUB.sh WH_MF_NM WH_NM_config $subjs 128GB

# WH_QSUB.sh WH_get_eves WH_NM_config $subjs 4GB 2400

# WH_QSUB.sh WH_epos WH_NM_config $subjs 16GB

# WH_QSUB.sh WH_covmat WH_NM_config $subjs 32GB

# WH_QSUB.sh WH_plot_cov WH_NM_config $subjs 1GB 4000

WH_QSUB.sh WH_evos WH_NM_config $subjs 2GB

WH_QSUB.sh WH_plot_evocurves WH_NM_config $subjs 1GB 0030

WH_QSUB.sh WH_plot_topos WH_NM_config $subjs 1GB 0030


# WH_QSUB.sh WH_FwdSol WH_NM_config $subjs 2GB

# WH_QSUB.sh WH_InvOp WH_NM_config $subjs 2GB 0030

# WH_QSUB.sh WH_AppInvOp WH_NM_config $subjs 1GB 0100


### General

# WH_QSUB.sh WH_plot_CoordTrans WH_MNE_config $subjs 1GB
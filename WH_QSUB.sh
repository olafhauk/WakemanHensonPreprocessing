#!/bin/bash

## wrapper script for MNE-Python analysis of Wakeman/Henson EMEG data
# e.g. WH_QSUB.sh WH_MF_MNE WH_MNE_config

# arguments:
# 1: python script
# 2: config script
# 3: subject numbers (e.g. 0-15)
# 4: memory (e.g. 32GB)
# 5: time delay for execution (HHMM), optional
# can only deal with one-day delays (across one midnight)

# python script to execute
py_script=$1

# configu file with analysis parameters
config=$2

# current working directory, from which to execute python script with config file
cwd=$(pwd)

# command to execute
py_command=$cwd"/"$py_script".py "$config

# files with qsub output
file_err="/home/olaf/MEG/WakemanHensonEMEG/qsub_out/"$py_script"_"$config".err"
file_out="/home/olaf/MEG/WakemanHensonEMEG/qsub_out/"$py_script"_"$config".out"

# delete existing output files
rm -f $file_err
rm -f $file_out

# indices of subjects to process (starting at 0)
subjs=$3

# requested memory and wall time
mem=$4
walltime="24:00:00"

# execution time
exe_t=$5

echo ""
echo "#########################################################################"
echo "###" $py_command
echo "#########################################################################"
echo $file_err
echo $file_out
echo $mem $walltime $subjs

if [ $# = 5 ]; then

    now=`date "+%H%M"`

    now=$((10#$now))

    # convert to decimal with base 10 (i.e. no trailing zeros)
    # for addition
    delay=$((10#$5))

    exe_t=$((now+$delay))

    # get hours and minutes
    hh=$((exe_t / 100))
    mm=$((exe_t % 100))

    hh=$((10#$hh)) # convert to decimal for additions
    mm=$((10#$mm))

    # if more minutes than an hour
    if (( mm >= 60 )); then
        hh=$((hh+1))
        mm=$((mm % 60))
    fi

    # if more hours than a day
    # note: qsub will start next day
    if (( hh >= 24 )); then
        hh=$((hh % 24))
    fi

    # get into right format with trailing zeros
    exe_t=$(printf "%02d%02d" $hh $mm)

    echo $(printf "Submitting at time: # %02d:%02d #\n" $hh $mm)

    qsub -a $exe_t -N "$py_script" -t $subjs -l walltime=$walltime,mem=$mem -o "$file_out" -e "$file_err" -v myvar="$py_command" /home/olaf/MEG/WakemanHensonEMEG/wrapper_python_cluster.sh
else
    hh=$((now / 100))
    mm=$((now % 100))
    echo $(printf "Submitting straightaway: # %02d:%02d #\n" $hh $mm)
    qsub -N "$py_script" -t $subjs -l walltime=$walltime,mem=$mem -o "$file_out" -e "$file_err" -v myvar="$py_command" /home/olaf/MEG/WakemanHensonEMEG/wrapper_python_cluster.sh
fi
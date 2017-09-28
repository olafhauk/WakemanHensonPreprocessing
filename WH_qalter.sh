#!/bin/bash

if [ $# = 0 ]; then
    echo
    echo "Utility function to change qsub parameters"
    echo "e.g. start time of waiting jobs"
    echo
    echo "Arguments:"
    echo "1: Job ID (qsub)"
    echo "2: qstat command to apply (e.g. \"-a 1600\", \"-l mem=16GB\")"
    echo "subject number(s) (e.g. 3, "1 5 10")"
    echo
    echo "e.g. WH_qalter.sh 2402085 \"-a 1600 -l mem=5GB\" \"0 1 2 11\""
    echo
    echo "OH August 2017"
    exit
fi


if [ $# = 2 ]; then
    subjs='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'
else
    subjs=$3
fi

for ss in $subjs;
do
    jobname=$1"-"$ss

    cmd_str="qalter "$2" "$jobname
    echo $cmd_str

    qalter $2 $jobname
done


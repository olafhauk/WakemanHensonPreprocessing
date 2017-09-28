#!/bin/bash

if [ $# = 0 ]; then
    echo
    echo "Utility function to delete individual qsub jobs"
    echo
    echo "Arguments:"
    echo "1: Job ID (qsub)"
    echo "2: how many successive jobs to delete"
    echo
    echo "OH August 2017"
    exit
fi

if [ $# = 1 ]; then
    subjs='0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'
else
    subjs=$2
fi

for ss in $subjs;
do
    jobname=$1"-"$ss

    cmd_str="qdel "$jobname
    echo $cmd_str

    qdel $jobname
done


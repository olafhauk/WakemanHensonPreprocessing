#!/bin/bash

if [ $# = 0 ]; then
    echo
    echo "Utility function to delete qsub processes"
    echo "each including multiple job IDs"
    echo
    echo "Arguments:"
    echo "1: Process ID (qsub, job ID without \"-??\")"
    echo "2: how many successive jobs to delete"
    echo
    echo "OH August 2017"
    exit
fi

if [ $# = 1 ]; then
    n=1
else
    n=$2
fi

procid=$1

for ((ii=procid; ii<$((procid+n)); ii+=1));
do
    
    cmd_str="qdel "$ii
    echo $cmd_str

    qdel $ii
done


#!/bin/bash

for dir in *
do
    if [ $dir != 'base/' ] && [ $dir != 'bezier_shapes/' ] && [ -d $dir ]; then
        echo "Submitting run from $dir"
        cd $dir
        sbatch --ntasks=16 --job-name=$dir submit.sh
        cd ..
    fi
done
echo "Ran all cases"
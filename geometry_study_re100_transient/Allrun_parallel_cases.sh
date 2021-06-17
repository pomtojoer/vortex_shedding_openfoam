#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ]; then
        echo "Starting run from $dir"
        ./$dir/Allrun_parallel
    fi
    echo "Completed run from $dir"
done
echo "Ran all cases"
#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ]; then
        echo "Starting run from $dir"
        ./$dir/Allclean
    fi
    echo "Completed run from $dir"
done
echo "Ran all cases"
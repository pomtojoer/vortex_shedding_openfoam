#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ] && [ $dir != 'bezier_shapes/' ]; then
        echo "Starting run from $dir"
        ./$dir/Allclean
    fi
    echo "Completed run from $dir"
done
echo "Ran all cases"
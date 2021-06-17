#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ] && [ $dir != 'bezier_shapes/' ]; then
        echo "Removing $dir"
        rm -r $dir
    fi
done
echo "Deleted all cases"
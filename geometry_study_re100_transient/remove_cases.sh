#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ]; then
        echo "Removing $dir"
        rm -r $dir
    fi
done
echo "Deleted all cases"
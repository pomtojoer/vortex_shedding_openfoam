#!/bin/bash

for dir in *
do
    if [ $dir != 'base/' ] && [ $dir != 'bezier_shapes/' ] && [ -d $dir ]; then
        echo "Cancelling run from $dir"
        scancel --name=$dir
    fi
done
echo "Cancelled all cases"
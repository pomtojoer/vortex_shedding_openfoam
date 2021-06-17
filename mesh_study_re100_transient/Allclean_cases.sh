#!/bin/bash

for dir in */
do
    if [ $dir != 'base/' ]; then
        echo "Starting clean from $dir"
        ./$dir/Allclean
    fi
    echo "Completed clean from $dir"
done
echo "Cleaned all cases"
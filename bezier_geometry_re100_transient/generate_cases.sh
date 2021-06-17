#!/bin/bash

if [ -z "$1" ]
  then
    echo "No argument supplied, exiting..."
    exit 1
fi

echo "generating data for $1 dataset"
if [ -d "$(pwd)"/bezier_shapes/$1 ] ; then
    # directory exists
    echo "Directory $1 exists, generating cases"
else
    # directory doesnt exists
    echo "Directory $1 doesn't exists, exiting..."
    exit 2
fi

mkdir $1
cp utils/* $1/

for file in "$(pwd)"/bezier_shapes/$1/meshes/*.msh
do 
    echo "******************** start ****************************"
    mesh_filename=$(basename $file)
    mesh_filepath=$file
    study_foldername=$(pwd)/$1/${mesh_filename/.msh/}
    if [ -d "$study_foldername" ]; then
        # directory exists
        echo "skipping $study_foldername, folder exists."
    else
        # directory doesnt exists
        cp -r base $study_foldername
    fi
    cp $mesh_filepath $study_foldername/obstacle.msh
    echo "geo mesh filename:$mesh_filename"
    echo "geo mesh filepath:$mesh_filepath"
    echo "geo study foldername:$study_foldername"
    echo "********************* end *****************************"
done
echo "Generated all 3D meshes"
#!/bin/bash

for file in "$(pwd)"/../models/mesh_study/*.msh
do 
    echo "******************** start ****************************"
    mesh_filename=$(basename $file)
    mesh_filepath=$file
    study_foldername=$(pwd)/${mesh_filename/.msh/}
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
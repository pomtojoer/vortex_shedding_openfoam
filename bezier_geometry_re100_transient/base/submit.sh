#!/bin/bash
#SBATCH --job-name=foam
#SBATCH --ntasks=108
#SBATCH --output=%x_%j.out

module load openmpi
source /fsx/OpenFOAM/OpenFOAM-v2012/etc/bashrc

# meshing from gmsh
gmshToFoam obstacle.msh  > ./log/gmshToFoam.log 2>&1

# changing patches
changeDictionary  > ./log/changeDictionary.log 2>&1

# checking mesh
checkMesh  > ./log/checkMesh.log 2>&1

# decomposing mesh
decomposePar -decomposeParDict system/decomposeParDict.ptscotch  > ./log/decomposePar.log 2>&1

# renumbers the cell list in order to reduce the bandwidth
mpirun -np $SLURM_NTASKS renumberMesh -parallel  -overwrite -noFunctionObjects -dict system/renumberMeshDict -decomposeParDict system/decomposeParDict.ptscotch  > ./log/renumberMesh.log 2>&1

# resetting initial
ls -d processor* | xargs -i rm -rf ./{}/0
ls -d processor* | xargs -i cp -r 0.orig ./{}/0

# solving
mpirun -np $SLURM_NTASKS pisoFoam -parallel  -decomposeParDict system/decomposeParDict.ptscotch > ./log/pisoFoam.log 2>&1


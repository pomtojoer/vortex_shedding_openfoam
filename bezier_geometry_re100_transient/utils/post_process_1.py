# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os

from multiprocessing import Pool
from itertools import repeat


def main():
    cwd = os.getcwd()
    geometry_directories = os.listdir(cwd)
    geometry_directories.sort()
    geometry_directories = [geometry_directory for geometry_directory in geometry_directories if os.path.isdir(os.path.join(cwd, geometry_directory))]

    with Pool(12) as p:
        p.starmap(paraview_postprocess_geometry_data_wrapper, zip(repeat(cwd), geometry_directories))

    print('############## SUMMARY ##############')
    for geometry_directory in geometry_directories:
        extracted_files_count = len(os.listdir(os.path.join(cwd, geometry_directory, 'extracts')))
        print(geometry_directory,extracted_files_count)
        

def paraview_postprocess_geometry_data_wrapper(cwd, geometry_directory):
    print(f'Extracting data as csv from {geometry_directory}')
    
    # Checking if foam case file exists, if not create one
    foam_case_filename = os.path.join(cwd, geometry_directory, f'{geometry_directory}.foam')
    try:
        open(foam_case_filename, 'x')
        print(f'Creating foam case file: {foam_case_filename}')
    except FileExistsError:
        pass

    # processing data
    response = paraview_postprocess_geometry_data(cwd, geometry_directory)
    if response:
        print(f'Extraction from {geometry_directory} SUCCESS', '\n')


def paraview_postprocess_geometry_data(cwd, geometry_directory):
    # create a new 'OpenFOAMReader'
    case_filename = f'{geometry_directory}.foam'
    case_filepath = os.path.join(cwd, geometry_directory, case_filename)
    shape_0foam = OpenFOAMReader(registrationName=case_filename, FileName=case_filepath)
    shape_0foam.MeshRegions = ['internalMesh']

    # Properties modified on shape_0foam
    shape_0foam.CaseType = 'Decomposed Case'

    UpdatePipeline(time=0.0, proxy=shape_0foam)

    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # create a new 'Clip'
    clip1 = Clip(registrationName='Clip1', Input=shape_0foam)
    clip1.ClipType = 'Plane'
    clip1.HyperTreeGridClipper = 'Plane'
    clip1.Scalars = ['POINTS', 'p']
    clip1.Value = -0.2905687689781189

    # init the 'Plane' selected for 'ClipType'
    clip1.ClipType.Origin = [7.5, 0.0, 0.5]

    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip1.HyperTreeGridClipper.Origin = [7.5, 0.0, 0.5]

    # Properties modified on clip1.ClipType
    clip1.ClipType.Origin = [-1.0, 0.0, 0.0]
    clip1.ClipType.Normal = [-1.0, 0.0, 0.0]

    UpdatePipeline(time=1.0, proxy=clip1)

    # Properties modified on shape_0foam
    shape_0foam.CellArrays = ['U', 'U_0', 'p', 'vorticity', 'yPlus']

    # create a new 'Clip'
    clip2 = Clip(registrationName='Clip2', Input=clip1)
    clip2.ClipType = 'Plane'
    clip2.HyperTreeGridClipper = 'Plane'
    clip2.Scalars = ['POINTS', 'p']
    clip2.Value = -0.2905687689781189

    # init the 'Plane' selected for 'ClipType'
    clip2.ClipType.Origin = [12.0, 0.0, 0.5]

    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip2.HyperTreeGridClipper.Origin = [12.0, 0.0, 0.5]

    # Properties modified on clip2.ClipType
    clip2.ClipType.Origin = [9.0, 0.0, 0.5]

    UpdatePipeline(time=1.0, proxy=clip2)

    # create a new 'Clip'
    clip3 = Clip(registrationName='Clip3', Input=clip2)
    clip3.ClipType = 'Plane'
    clip3.HyperTreeGridClipper = 'Plane'
    clip3.Scalars = ['POINTS', 'p']
    clip3.Value = -0.2905687689781189

    # init the 'Plane' selected for 'ClipType'
    clip3.ClipType.Origin = [4.0, 0.0, 0.5]

    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip3.HyperTreeGridClipper.Origin = [4.0, 0.0, 0.5]

    # Properties modified on clip3.ClipType
    clip3.ClipType.Origin = [0.0, 2.0, 0.0]
    clip3.ClipType.Normal = [0.0, 1.0, 0.0]

    UpdatePipeline(time=1.0, proxy=clip3)

    # create a new 'Clip'
    clip4 = Clip(registrationName='Clip4', Input=clip3)
    clip4.ClipType = 'Plane'
    clip4.HyperTreeGridClipper = 'Plane'
    clip4.Scalars = ['POINTS', 'p']
    clip4.Value = -0.2905687689781189

    # init the 'Plane' selected for 'ClipType'
    clip4.ClipType.Origin = [4.0, -4.0, 0.5]

    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip4.HyperTreeGridClipper.Origin = [4.0, -4.0, 0.5]

    # Properties modified on clip4.ClipType
    clip4.ClipType.Origin = [0.0, -2.0, 0.0]
    clip4.ClipType.Normal = [0.0, -1.0, 0.0]

    UpdatePipeline(time=1.0, proxy=clip4)

    # create a new 'Resample To Image'
    resampleToImage1 = ResampleToImage(registrationName='ResampleToImage1', Input=clip4)
    resampleToImage1.SamplingBounds = [-1.0, 9.0, -2.0, 2.0, 0.0, 1.0]

    # Properties modified on resampleToImage1
    resampleToImage1.SamplingDimensions = [500, 200, 1]

    UpdatePipeline(time=1.0, proxy=resampleToImage1)

    # create a new 'Clean to Grid'
    cleantoGrid1 = CleantoGrid(registrationName='CleantoGrid1', Input=resampleToImage1)

    UpdatePipeline(time=1.0, proxy=cleantoGrid1)

    # create extractor
    cSV1 = CreateExtractor('CSV', cleantoGrid1, registrationName='CSV1')

    # save extracts
    extracts_output_directory = os.path.join(cwd,geometry_directory, 'extracts')
    SaveExtracts(ExtractsOutputDirectory=extracts_output_directory,
        GenerateCinemaSpecification=0)

    return True


if __name__ == '__main__':
    main()
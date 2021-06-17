from multiprocessing import Pool
from itertools import repeat

import numpy as np
import pandas as pd

import os

import matplotlib.pyplot as plt
import cmocean

from progress.bar import Bar

import json


def main():
    cwd = os.getcwd()
    geometry_directories = os.listdir(cwd)
    geometry_directories.sort()
    geometry_directories = [geometry_directory for geometry_directory in geometry_directories if os.path.isdir(os.path.join(cwd, geometry_directory)) and geometry_directory!='base']
    
    dst_parent_folder = os.path.join('/fsx/python_ml/flow_reconstruction/data', 'primitives')
    if not os.path.isdir(dst_parent_folder):
        os.mkdir(dst_parent_folder)
        print(f'Created destination parent folder: {dst_parent_folder}')

    error_dict = {}
    for geometry_directory in geometry_directories:
        print(f'Cleaning {geometry_directory}')
        error_arr = clean_geometry_data(cwd, dst_parent_folder, geometry_directory)
        error_dict[geometry_directory] = error_arr

    post_processing_error_file = 'post_processing_error.json'
    if not os.path.isfile(post_processing_error_file):
        with open(post_processing_error_file, 'w') as f:
            json.dump(error_dict, f, indent=4)
    else:
        with open(post_processing_error_file, 'r') as f:
            prev_error_dict = json.load(f)
            combined_error_dict = {**error_dict, **prev_error_dict}
        with open(post_processing_error_file, 'w') as f:
            json.dump(combined_error_dict, f, indent=4)


def clean_geometry_data(cwd, dst_parent_folder, geometry_directory):
    src_folder = os.path.join(cwd, geometry_directory, 'extracts')
    dst_folder = os.path.join(dst_parent_folder, geometry_directory)

    # creating save folder
    if not os.path.isdir(dst_folder):
        os.mkdir(dst_folder)
        print(f'Created directory: {dst_folder}')
    else:
        dst_folder_count = len(os.listdir(dst_folder))
        if dst_folder_count == 6:
            print(f'Previously converted: {geometry_directory}')
            return []

    csv_files = [os.path.join(cwd, geometry_directory, 'extracts', src_csv) for src_csv in os.listdir(src_folder)]
    csv_files.sort()

    if len(csv_files) != 500:
        print('ERROR: not 500 csv files')
        return False
    else:
        print('Extracting data')

    ny = 200
    nx = 500

    w_z = np.zeros((len(csv_files), ny, nx))
    u_x = np.zeros((len(csv_files), ny, nx))
    u_y = np.zeros((len(csv_files), ny, nx))
    geometry_binary = np.zeros((ny,nx))

    error_arr = []

    bar = Bar('Processing', max=len(csv_files))
    for idx, csv_file in enumerate(csv_files):
        data = pd.read_csv(csv_file)
        try:
            w_z[idx,:,:] = data['vorticity:2'].to_numpy().reshape(ny, nx)
            u_x[idx,:,:] = data['U:0'].to_numpy().reshape(ny, nx)
            u_y[idx,:,:] = data['U:1'].to_numpy().reshape(ny, nx)
        except KeyError:
            print(f'ERROR @ {idx}: KEY ERROR')
            error_arr.append(idx)
        if idx == 0:
            geometry_binary = data['vtkValidPointMask'].to_numpy().reshape(ny, nx)

        bar.next()
    bar.finish()
    
    u_mag = np.sqrt(np.square(u_x)+np.square(u_y))

    bar = Bar('Saving', max=5)
    with open(os.path.join(dst_folder, 'w_z.npy'), 'wb') as f:
        np.save(f, w_z)
        bar.next()
    with open(os.path.join(dst_folder, 'u_x.npy'), 'wb') as f:
        np.save(f, u_x)
        bar.next()
    with open(os.path.join(dst_folder, 'u_y.npy'), 'wb') as f:
        np.save(f, u_y)
        bar.next()
    with open(os.path.join(dst_folder, 'geo_bin.npy'), 'wb') as f:
        np.save(f, geometry_binary)
        bar.next()
    with open(os.path.join(dst_folder, 'u_mag.npy'), 'wb') as f:
        np.save(f, u_mag)
        bar.next()
    bar.finish()

    print('plotting')
    sample_idx = 0

    w_z_sample = w_z[sample_idx]
    u_x_sample = u_x[sample_idx]
    u_y_sample = u_y[sample_idx]
    u_mag_sample = u_mag[sample_idx]

    x = np.arange(0, nx, 1)
    y = np.arange(0, ny, 1)
    mX, mY = np.meshgrid(x, y)

    fig, axs = plt.subplots(5, 1,facecolor="white",  edgecolor='k', figsize=(15.8,47))
    axs[0].imshow(geometry_binary)
    axs[0].set_title('Geometry with binary representation')
    
    minmax = np.max(np.abs(w_z_sample)) * 0.65
    axs[1].imshow(w_z_sample, cmap=cmocean.cm.balance, interpolation='none', vmin=-minmax, vmax=minmax)
    axs[1].contourf(mX, mY, w_z_sample, 80, cmap=cmocean.cm.balance, alpha=1, vmin=-minmax, vmax=minmax)
    axs[1].set_title(f'{geometry_directory} w_z. min: {w_z.min()}, max: {w_z.max()}, mean: {w_z.mean()}')
    
    minmax = np.max(np.abs(u_x_sample)) * 0.65
    axs[2].imshow(u_x_sample, cmap=cmocean.cm.balance, interpolation='none', vmin=-minmax, vmax=minmax)
    axs[2].contourf(mX, mY, u_x_sample, 80, cmap=cmocean.cm.balance, alpha=1, vmin=-minmax, vmax=minmax)
    axs[2].set_title(f'{geometry_directory} u_x. min: {u_x.min()}, max: {u_x.max()}, mean: {u_x.mean()}')

    minmax = np.max(np.abs(u_y_sample)) * 0.65
    axs[3].imshow(u_y_sample, cmap=cmocean.cm.balance, interpolation='none', vmin=-minmax, vmax=minmax)
    axs[3].contourf(mX, mY, u_y_sample, 80, cmap=cmocean.cm.balance, alpha=1, vmin=-minmax, vmax=minmax)
    axs[3].set_title(f'{geometry_directory} u_y. min: {u_y.min()}, max: {u_y.max()}, mean: {u_y.mean()}')

    minmax = np.max(np.abs(u_mag_sample)) * 0.65
    axs[4].imshow(u_mag_sample, cmap=cmocean.cm.balance, interpolation='none', vmin=-minmax, vmax=minmax)
    axs[4].contourf(mX, mY, u_mag_sample, 80, cmap=cmocean.cm.balance, alpha=1, vmin=-minmax, vmax=minmax)
    axs[4].set_title(f'{geometry_directory} u_mag. min: {u_mag.min()}, max: {u_mag.max()}, mean: {u_mag.mean()}')
    
    plt.savefig(os.path.join(dst_folder, 'output_sample.png'))

    print(f'finished {geometry_directory}')

    return error_arr

if __name__ == '__main__':
    main()
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    cwd = os.getcwd()
    geometry_directories = os.listdir(cwd)
    geometry_directories.sort()
    geometry_directories = [geometry_directory for geometry_directory in geometry_directories if os.path.isdir(os.path.join(cwd, geometry_directory))]

    for geometry_directory in geometry_directories:
        extracts_directory = os.path.join(cwd, geometry_directory, 'extracts')
        extracts_count = len(os.listdir(extracts_directory))

        npy_directory = os.path.join('/fsx/python_ml/flow_reconstruction/data', cwd.split('/')[-1], geometry_directory)
        if os.path.isdir(npy_directory):
            npy_count = len(os.listdir(npy_directory))
        else:
            npy_count = 0
        
        if extracts_count != 500 or npy_count != 6:
            print(f'{bcolors.FAIL}{geometry_directory:<10}    csv - {extracts_count:<3}/500    npy - {npy_count:<1}/6{bcolors.ENDC}')
        else:
            print(f'{geometry_directory:<10}    csv - {extracts_count:<3}/500    npy - {npy_count:<1}/6')


if __name__ == '__main__':
    main()
import os
import argparse
import subprocess
from glob import glob


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', '-i', required=True)
    parser.add_argument('--outdir', '-o', required=True)
    parser.add_argument('--all', '-a', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    if args.all:
        data_from = os.path.join(args.indir, '*.wav')
    else:
        data_from = os.path.join(args.indir, '*000*.wav')
    data_list = glob(data_from)
    os.makedirs(args.outdir)
    for data in data_list:
        subprocess.call(['cp', data, args.outdir])

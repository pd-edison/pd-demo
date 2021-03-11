import os
import argparse
import subprocess

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indir', '-i', required=True)
    parser.add_argument('--outdir', '-o', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    data_from = os.path.join(args.indir, '*000*.wav')
    subprocess.call(['cp', data_from, args.outdir])
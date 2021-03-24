import os
from glob import glob

import yaml
import numpy as np
from jinja2 import FileSystemLoader, Environment


def gen_gender_items(gender):
    ret = []
    data_dirs = glob(os.path.join(f'data/{gender}/*'))
    info = yaml.safe_load(open(f'data/{gender}/info.yaml', 'r'))
    transcriptions = info.pop('transcriptions')
    titles = []
    gops = []
    wavss = []
    for data_dir in data_dirs:
        if os.path.isfile(data_dir):
            continue
        name = os.path.basename(data_dir)
        data_info = info.pop(name)
        title = data_info.pop('title', name)
        gop = data_info.pop('gop', '-')
        wavs = sorted(glob(os.path.join(data_dir, '*.wav')))
        titles.append(title)
        gops.append(gop)
        wavss.append(wavs)
    wavss = np.array(wavss).T
    meta = {
        'titles': titles,
        'gops': gops,
        'transcriptions': transcriptions,
        'wavss': wavss,
    }
    return meta


def gen_vocoder_items():
    ret = []
    info = yaml.safe_load(open('data/vocoder/info.yaml', 'r'))
    # data_dirs = glob(os.path.join('data/vocoder/*'))
    use_vocoders = info.pop('use_vocoders')
    use_files = info.pop('use_files')
    data_dirs = [os.path.join('data/vocoder', use_vocoder) for use_vocoder in use_vocoders]
    titles = ['raw']
    wavs = [os.path.join('raw', use_file+'.wav') for use_file in use_files]
    wavss = [wavs]
    for data_dir in data_dirs:
        if os.path.isfile(data_dir):
            continue
        name = os.path.basename(data_dir)
        # wavs = sorted(glob(os.path.join(data_dir, '*.wav')))
        wavs = [os.path.join(data_dir, use_file+'_gen.wav') for use_file in use_files]
        titles.append(name)
        wavss.append(wavs)
    wavss = np.array(wavss, dtype=object).T
    meta = {
        'titles': titles,
        'use_files': use_files,
        'wavss': wavss,
    }
    return meta


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    env.globals.update(zip=zip, len=len)
    template = env.get_template("pd.html.jinja2")

    male_items = gen_gender_items('male')
    vocoder_items = gen_vocoder_items()

    html = template.render(
        male_items=male_items,
        vocoder_items=vocoder_items,
    )
    print(html)

if __name__ == "__main__":
    main()
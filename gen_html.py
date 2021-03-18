import os
from glob import glob

import yaml
import numpy as np
from jinja2 import FileSystemLoader, Environment


def gen_block_items():
    ret = []
    data_dirs = glob(os.path.join('data/*'))
    transcriptions = yaml.safe_load(open('data/transcriptions.yaml', 'r'))['data']
    titles = []
    gops = []
    wavss = []
    for data_dir in data_dirs:
        if os.path.isfile(data_dir):
            continue
        info = yaml.safe_load(open(os.path.join(data_dir, 'info.yaml'), 'r'))
        title = info.pop('title', os.path.basename(data_dir))
        gop = info.pop('gop', '-')
        wavs = sorted(glob(os.path.join(data_dir, '*.wav')))
        titles.append(title)
        gops.append(gop)
        wavss.append(wavs)
    wavss = np.array(wavss).T
    return titles, gops, transcriptions, wavss

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    env.globals.update(zip=zip, len=len)
    template = env.get_template("pd.html.jinja2")

    # block_items = gen_block_items()
    titles, gops, transcriptions, wavss = gen_block_items()

    html = template.render(
        # block_items=block_items,
        titles=titles,
        gops=gops,
        transcriptions=transcriptions,
        wavss=wavss,
    )
    print(html)

if __name__ == "__main__":
    main()
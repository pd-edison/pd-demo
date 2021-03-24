import os
from glob import glob

import yaml
import numpy as np
from jinja2 import FileSystemLoader, Environment


def gen_male_items():
    ret = []
    data_dirs = glob(os.path.join('data/male/*'))
    info = yaml.safe_load(open('data/male/info.yaml', 'r'))
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


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    env.globals.update(zip=zip, len=len)
    template = env.get_template("pd.html.jinja2")

    # block_items = gen_block_items()
    male_items = gen_male_items()

    html = template.render(
        # block_items=block_items,
        male_items=male_items,
    )
    print(html)

if __name__ == "__main__":
    main()
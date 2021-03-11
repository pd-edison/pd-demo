import os
from glob import glob

import yaml
from jinja2 import FileSystemLoader, Environment


def gen_block_items():
    ret = []
    data_dirs = glob(os.path.join('data/*'))
    transcriptions = yaml.safe_load(open('data/transcriptions.yaml', 'r'))['data']

    for data_dir in data_dirs:
        if os.path.isfile(data_dir):
            continue
        info = yaml.safe_load(open(os.path.join(data_dir, 'info.yaml'), 'r'))
        title = info.pop('title', os.path.basename(data_dir))
        gop = info.pop('gop', '-')
        wavs = sorted(glob(os.path.join(data_dir, '*.wav')))
        item = (
                title,
                gop,
                wavs,
                transcriptions,
            )
        ret.append(item)
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    env.globals.update(zip=zip)
    template = env.get_template("base.html.jinja2")

    block_items = gen_block_items()

    html = template.render(
        block_items=block_items,
    )
    print(html)

if __name__ == "__main__":
    main()
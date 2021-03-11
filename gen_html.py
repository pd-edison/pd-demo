import os
from glob import glob

import yaml
from jinja2 import FileSystemLoader, Environment


def gen_block_items():
    ret = []
    data_dirs = glob(os.path.join('data/*'))

    for data_dir in data_dirs:
        info = yaml.safe_load(open(os.path.join(data_dir, 'info.yaml')))
        title = info.pop('title', os.path.basename(data_dir))
        gop = info.pop('gop', '-')
        wavs = glob(os.path.join(data_dir, '*.wav'))
        item = (
                title,
                gop,
                wavs,
            )
        ret.append(item)
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    block_items = gen_block_items()

    html = template.render(
        block_items=block_items,
    )
    print(html)

if __name__ == "__main__":
    main()
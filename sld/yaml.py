from pathlib import Path

import yaml


def open_yaml(yaml_file: Path) -> dict:
    with open(yaml_file) as f:
        yaml_contents = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_contents

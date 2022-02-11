from pathlib import Path
from sld.yaml import open_yaml

data_dir = Path.cwd() / "tests" / "data"
test_yaml = data_dir / "test.yaml"


def test_open_yaml():
    yaml_contents = open_yaml(test_yaml)
    assert False


from pathlib import Path
from sld.yaml import open_yaml

data_dir = Path.cwd() / "tests" / "data"
test_yaml = data_dir / "test.yaml"


def test_open_yaml():
    yaml_contents = open_yaml(test_yaml)
    assert len(yaml_contents) == 4
    assert yaml_contents["a"] == 1
    assert yaml_contents["b"] == 2
    assert yaml_contents["c"] == "three"
    assert len(yaml_contents["TestClass"]) == 2
    assert yaml_contents["TestClass"]["ClassName"] == "TestClass"
    assert yaml_contents["TestClass"]["num"] == 200

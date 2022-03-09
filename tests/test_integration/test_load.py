from pathlib import Path

from sld import SlideBook

data_dir = Path.cwd() / "tests" / "data"

test_sldy = data_dir / "sldy.sldy"


def test_load_sldy():
    sld = SlideBook(test_sldy)

    assert sld.number_acquisitions == 1

    assert len(sld.images) == 1
    assert sld.images[0].num_channels == 8
    assert len(sld.images[0].channels) == sld.images[0].num_channels
    assert len(sld.images[0].data) == sld.images[0].num_channels
    assert len(sld.images[0].histogram_summaries) == sld.images[0].num_channels

    assert sld.images[0].data["ch_0"][0].shape == (4, 1024, 1024)
    assert sld.images[0].data["ch_0"][0][2, 10, 10] == 152

    assert sld.images[0].name == "StageScan1643299934"

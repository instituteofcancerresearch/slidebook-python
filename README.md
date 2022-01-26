**Work in progress**
# slidebook-python
Open slidebook .sldy files in Python

### To install
**`slidebook-python` requires Python >= 3.9**
```bash
pip install slidebook-python
```

### To use
```python
from sld import SlideBook
sld = SlideBook("/path/to/file.sldy")

# How many acquisitions
print(sld.number_acquisitions)
# 4

# How many channels in first acquisition
print(sld.images[0].num_channels)

# Get data from channel 0 of the second acquisition
data = sld.images[1].data["ch_0"]
```

### To visualise in napari
**N.B. napari plugin is in development**
```python
import napari
import numpy as np
from sld import SlideBook
sld = SlideBook("/path/to/file.sldy")
viewer = napari.Viewer()
viewer.add_image((np.squeeze(sld.images[0].data["ch_0"])), name="Channel 0")
viewer.add_image((np.squeeze(sld.images[0].data["ch_1"])), name="Channel 1")
napari.run()
```


By default, `Slidebook` will not load image data into memory. To force this, use `mmap_mode=None`:
```python
sld = SlideBook("/path/to/file.sldy", mmap_mode=None)
```
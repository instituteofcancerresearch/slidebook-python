from typing import TYPE_CHECKING, Union

import numpy as np

if TYPE_CHECKING:
    import dask.array

ArrayLike = Union[np.ndarray, "dask.array.Array"]

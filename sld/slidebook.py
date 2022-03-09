from pathlib import Path
from typing import Generator, Literal, Union

import dask.array as da
import numpy as np

from sld.yaml import open_yaml


class HistogramSummary:
    def __init__(
        self,
        histogram_summary_filename: Path,
        mmap_mode: Union[
            None, Literal["r+"], Literal["r"], Literal["w+"], Literal["c"]
        ] = "r",
    ):

        self._histogram_summary_filename = histogram_summary_filename
        try:
            self.histogram_summary = np.load(
                self._histogram_summary_filename,
                mmap_mode=mmap_mode,
            )
        except ValueError:
            self.histogram_summary = None
        self.channel = self._histogram_summary_filename.stem.split("_Ch")[-1]


class ImageMetadata:
    def __init__(self, image_directory: Path):
        self.annotation_record = open_yaml(
            image_directory / "AnnotationRecord.yaml"
        )
        self.aux_data = open_yaml(image_directory / "AuxData.yaml")
        self.channel_record = open_yaml(image_directory / "ChannelRecord.yaml")
        self.elapsed_times = open_yaml(image_directory / "ElapsedTimes.yaml")
        self.image_record = open_yaml(image_directory / "ImageRecord.yaml")
        self.mask_record = open_yaml(image_directory / "MaskRecord.yaml")
        self.sa_position_data = open_yaml(
            image_directory / "SAPositionData.yaml"
        )
        self.stage_position_data = open_yaml(
            image_directory / "StagePositionData.yaml"
        )


class ImageDirectory:
    def __init__(
        self,
        image_directory: Path,
        mmap_mode: Union[
            None, Literal["r+"], Literal["r"], Literal["w+"], Literal["c"]
        ] = "r",
    ):
        self._directory = image_directory
        self.name = self._directory.stem
        self.metadata = ImageMetadata(self._directory)
        self.histogram_summaries = [
            HistogramSummary(histogram_summary_filename, mmap_mode=mmap_mode)
            for histogram_summary_filename in self._directory.glob(
                "HistogramSummary_Ch*.npy"
            )
        ]
        self.channels = [
            histogram_summary.channel
            for histogram_summary in self.histogram_summaries
        ]
        self.num_channels = len(self.channels)

        self._data_paths = {
            f"ch_{channel}": self._directory.glob(
                f"ImageData_Ch{channel}*.npy"
            )
            for channel in self.channels
        }

        self.data = {
            data_path[0]: self.load_channel(data_path[1], mmap_mode=mmap_mode)
            for data_path in self._data_paths.items()
        }

    @staticmethod
    def load_channel(
        filenames: Generator[Path, None, None],
        mmap_mode: Union[
            None, Literal["r+"], Literal["r"], Literal["w+"], Literal["c"]
        ] = "r",
        filename_suffix: str = ".npy",
    ) -> list:
        array_list = []
        for filename in filenames:
            if filename.suffix == filename_suffix:
                array_list.append(np.load(filename, mmap_mode=mmap_mode))

        if mmap_mode is None:
            array = np.array(array_list)
        else:
            array = da.stack(array_list, axis=0)

        return array


def filter_image_directories(image_directories, filename_filters):
    new_dirs = []

    for image_dir in image_directories:
        if not any(filter in image_dir.name for filter in filename_filters):
            new_dirs.append(image_dir)

    return new_dirs


class SlideBook:
    def __init__(
        self,
        filename: Union[str, Path],
        mmap_mode: Union[
            None, Literal["r+"], Literal["r"], Literal["w+"], Literal["c"]
        ] = "r",
        filename_filters: list = ["MIP"],
    ):
        self._filename = Path(filename)
        self._data_directory = self._filename.with_suffix(".dir")

        self._image_directories = self._data_directory.glob("*.imgdir")
        self._image_directories = filter_image_directories(
            self._image_directories, filename_filters
        )

        self.images = [
            ImageDirectory(image_dir, mmap_mode=mmap_mode)
            for image_dir in self._image_directories
        ]
        self.number_acquisitions = len(self.images)

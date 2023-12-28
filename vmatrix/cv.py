from pathlib import Path
from typing import Union

import cv2
import numpy as np


class NoneImageError(Exception):
    pass


def imread(
    filepath: Union[str, Path],
    flags=cv2.IMREAD_UNCHANGED,
    dtype=np.uint8,
):
    """cv2.imread alternative for Korean filepath"""

    n = np.fromfile(filepath, dtype)
    img = cv2.imdecode(n, flags)

    if img is None:
        raise NoneImageError(f"{filepath} is None image")

    return img


def makedirs_if_not_exists(filepath: Union[str, Path]):
    if not isinstance(filepath, (str, Path)):
        raise TypeError(f"filepath must be a str or Path, but it's {type(filepath)}.")

    if isinstance(filepath, str):
        filepath = Path(filepath)

    if isinstance(filepath, Path):
        directory = filepath if filepath.is_dir() else filepath.parent
    if not directory.exists():
        directory.mkdir()


def write(filepath: Union[str, Path], img: np.ndarray):
    """cv2.imwrite alternative for Korean filepath"""

    if isinstance(filepath, str):
        filepath = Path(filepath)

    retval, buf = cv2.imencode(filepath.suffix, img)

    if retval:
        makedirs_if_not_exists(filepath)
        with open(filepath, mode="wb") as f:
            buf.tofile(f)
            return True
    else:
        return False


def contains_alpha_channel(image: np.ndarray):
    """Check image contains alpha channel"""

    if not isinstance(image, np.ndarray):
        raise ValueError(f"image is NOT np.ndarray: {type(image)}")

    if len(image.shape) == 3 and image.shape[-1] == 4:
        return True

    return False

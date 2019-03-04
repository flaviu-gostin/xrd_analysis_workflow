"""This script contains a function to extract one individual diffraction image from the one dataset inside hdf files as a numpy array.

Use: from get_slice import get_slice

"""

import h5py
import numpy as np


def get_slice(file, n):
    """First slice is 0, second is 1, ..."""
    all_slices = file['entry/instrument/detector/data']
    slice = all_slices[n]
    return slice


def test_slice():
    """Test function get_slice(file, n)"""
    file = h5py.File('../../../data/cmos-72532_FOR_TESTS.hdf', 'r')
    a_slice = get_slice(file, 71)
    assert a_slice.ndim == 2
    assert a_slice.shape == (2045, 4098)
    assert a_slice.dtype == 'uint16'


if __name__ == "__main__":
    print("Running tests")
    test_slice()
    print("Finished")

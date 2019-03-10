"""This script contains a function to extract one individual diffraction image from the one dataset inside hdf files as a numpy array.

Use: from get_slice import get_slice

"""

import h5py
import numpy as np


def get_slice(filename, n):
    """Extract one single slice from a .hdf file.  Counting starts at 0."""
    file = h5py.File(filename, 'r')
    dataset = file['entry/instrument/detector/data']
    slice = dataset[n]
    file.close()
    return slice


def test_get_slice():
    """Test function get_slice"""
    filename = "../dataset_for_tests.hdf"
    a_slice = get_slice(filename, 0)
    assert a_slice.ndim == 2
    assert a_slice.shape == (2045, 4098)
    assert a_slice.dtype == 'uint16'


if __name__ == "__main__":
    print("Running tests")
    test_get_slice()
    print("Finished")

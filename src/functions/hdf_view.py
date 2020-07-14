""" This script contains a function to extract one individual diffraction image
from the one dataset inside hdf files as a numpy array.

Use: from hdf_view import get_slice

"""

import h5py


def get_slice(filename, dataset_path, n):
    """Extract one single slice from a .hdf file.  Counting starts at 0."""
    file = h5py.File(filename, 'r')
    dataset = file[dataset_path]
    slice = dataset[n]
    file.close()
    return slice

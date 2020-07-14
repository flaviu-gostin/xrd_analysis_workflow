""" Test functions in hdf_view module.

Run from project root with: python -m pytest [src/tests/test_hdf_view.py]

"""
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from hdf_view import get_slice
sys.path.append(os.path.join(os.path.dirname(__file__), "../../data/"))
import inside_hdf


test_data_path = os.path.join(os.path.dirname(__file__), "test_data.hdf")
dataset_path = inside_hdf.hdf_dataset_path

def test_get_slice():
    """ Test function get_slice """
    slice = get_slice(test_data_path, dataset_path, 0)
    assert slice.ndim == 2
    assert slice.shape == (2045, 4098)
    assert slice.dtype == 'uint16'

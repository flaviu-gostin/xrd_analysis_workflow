""" Test functions in hdf_ops module.

Run from project root with: python -m pytest [src/tests/test_hdf_ops.py]

"""
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from hdf_ops import get_diffraction_image
sys.path.append(os.path.join(os.path.dirname(__file__), "../../data/"))
import inside_hdf


test_data_path = os.path.join(os.path.dirname(__file__), "test_data.hdf")
dataset_path = inside_hdf.hdf_dataset_path

def test_get_diffraction_image():
    """ Test function get_diffraction_image """
    image = get_diffraction_image(test_data_path, dataset_path, 0)
    assert image.ndim == 2
    assert image.shape == (2045, 4098)
    assert image.dtype == 'uint16'

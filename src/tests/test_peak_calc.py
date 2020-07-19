""" Test functions in peak_calc module.

Run from project root with: python -m pytest [src/tests/test_peak_calc.py]

"""
import numpy as np
import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from peak_calc import latt_ct_cubic, peak_position


test_file = os.path.join(os.path.dirname(__file__),
                         "twotheta-intensity_tests.dat")


def test_latt_ct_cubic():
    """ Test funtion latt_ct_cubic() """
    d_test0 = latt_ct_cubic(1e-10, 60, (1, 0, 0))

    #test the calculation is correct
    assert d_test0 == pytest.approx(1)

    #test ValueError exception is raised if wavelength has unexpected value
    with pytest.raises(ValueError):
        latt_ct_cubic(1, 60, (1, 0, 0))


def test_peak_position():
    """ Test function peak_position() """
    data = np.loadtxt(test_file)
    two_theta_interval = [33.5, 34.6]
    expect_val = 34.24808
    assert peak_position(data, two_theta_interval) == pytest.approx(expect_val,
                                                                    abs=0.001)
    with pytest.raises(TypeError):
        peak_position("fg", [5.6, 8.9])
    with pytest.raises(ValueError):
        a = np.arange(24).reshape(2, 3, 4)
        peak_position(a, [5.6, 8.9])
    with pytest.raises(TypeError):
        peak_position(data, (3.5, 9.8)) #2nd argument should be a list
    with pytest.raises(ValueError):
        peak_position(data, [5.6, 8.9, 7])

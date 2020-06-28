"""Functions to determine peak position and lattice constant."""

import numpy as np
import pytest
import os
import natsort


def latt_ct_cubic(wavelength, peak_pos, planes):
    """Calculate lattice constant of cubic systems.

    Calculate the lattice constant for a cubic lattice from the position of
    given peak position as 2theta and given hkl plane using Bragg's law and
    simple geometry. Note: you should make sure the hkl plane is the right one
    for the selected peak.

    Parameters
    ----------
    wavelength : float
        The value of the wavelength in meter used to measure the
        diffraction pattern.
    peak_pos : float
        The 2theta position of the diffraction peak in degree.
    planes : tuple
        Tuple with 3 integers representing the Miller indices (h, k, l)
        of the planes used for calculating the lattice constant.


    Returns
    -------
    a : float
        Value of lattice constant.

    """
    if wavelength < 1e-12 or wavelength > 1e-9:
        raise ValueError(str(wavelength) + " (meter) is an unlikely\
        value for the wavelength")

    # Change unit to Angstrom
    wl = wavelength * 1e+10
    # Calculate theta in radian
    theta = ((peak_pos / 2) * np.pi ) / 180
    # d is interplanar spacing from Bragg's law
    d = wl / (2 * np.sin(theta))
    # a is lattice constant
    a = d * np.sqrt(planes[0]**2 + planes[1]**2 + planes[2]**2)
    return a


def peak_position(pattern, two_theta_interval):
    """Determine peak position as the highest point in given interval.

    Determine peak position as the 2theta value of the data point with the
    highest intensity among all the data points in given interval.

    Parameters
    ----------
    pattern : ndarray
        Numpy 2 dimensional array. Two-theta values are in pattern[:,0] and
        intensity values are in pattern[:,1]
    two_theta_interval : list
        Two two-theta values, one at the onset and one at the end of a
        diffraction peak.

    Returns
    -------
    peak_position : float
        Two-theta value of peak position.

    """
    if not isinstance(pattern, np.ndarray):
        raise TypeError("'pattern' must be a numpy array")

    if pattern.ndim != 2 or len(pattern[0]) != 2:
        raise ValueError("'pattern' must have 2 dimensions, and 2nd dimension \
                         must have 2 elements")

    if not isinstance(two_theta_interval, list):
        raise TypeError("'two_theta_interval' must be a list")

    if len(two_theta_interval) != 2:
        raise ValueError("this list must have exactly 2 members")

    two_theta_interval = [float(i) for i in two_theta_interval]
    st_idx, end_idx = np.searchsorted(pattern[:,0], two_theta_interval)
    intensity_slice = pattern[st_idx:end_idx, 1]
    idx_max_intensity = np.argmax(intensity_slice) + st_idx
    return pattern[idx_max_intensity, 0]


def test_latt_ct_cubic():
    d_test0 = latt_ct_cubic(1e-10, 60, (1, 0, 0))
    #test the calculation is correct
    assert d_test0 == pytest.approx(1)
    #test ValueError exception is raised if wavelength has unexpected value
    with pytest.raises(ValueError):
        latt_ct_cubic(1, 60, (1, 0, 0))


def test_peak_position():
    test_file = '../twotheta-intensity_tests.dat'
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

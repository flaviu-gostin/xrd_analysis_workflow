"""Functions to determine peak position and lattice constant."""

import numpy as np
import os
import natsort


def latt_ct_cubic(wavelength, peak_pos, hkl):
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
    hkl : tuple
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
    a = d * np.sqrt(hkl[0]**2 + hkl[1]**2 + hkl[2]**2)
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

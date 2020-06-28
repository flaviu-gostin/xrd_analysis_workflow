"""Calculate lattice constant from peak position"""

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


def peak_maxima(dir_1D, patterns, tth_interval):
    """Determine two-theta of peak maximum for given patterns.

    For each given pattern determine the two-theta value of the highest
    intensity in the given interval.  Note: it is assumed that the two-theta
    axis is the same for all patterns, i.e. patterns[0][..., 0] ==
    patterns[1][..., 0] == ...

    Parameters
    ----------
    dir_1D : string
        Directory where the 1D diffraction pattern are
    patterns : tuple
        Tuple with 2 integers (first pattern, last pattern + 1)
    tth_interval : tuple
        Tuple with 2 float objects representing the left and right
        margins of the two-theta interval in which the peak is located.

    Returns
    -------
    twotheta_peaks : list
        List containing two-theta values in degrees, one value for each
        pattern.  Each value corresponds to the maximum intensity in the
        given interval.

    """
    # twotheta_peaks is a list collecting peak maxima
    twotheta_peaks = []
    # Use the 1st pattern to determine indices of tth_interval
    patt0 = np.loadtxt(dir_1D + str(patterns[0]) + ".dat",
                       usecols=(0,1))
    st = get_idx(patt0, tth_interval[0])
    end = get_idx(patt0, tth_interval[1])
    # List of files (each file contains a pattern) sorted numerically
    files = \
    natsort.natsorted(os.listdir(dir_1D))[patterns[0]:patterns[1]]
    for file in files:
        pattern_whole = np.loadtxt(dir_1D + file, usecols=(0, 1))
        # roi is a slice containing the Pd113 region
        roi = pattern_whole[st:end, : ]
        i_max_idx = np.argmax(roi[..., 1])    # Index of maximum intensity
        twotheta_peak = roi[i_max_idx, 0]
        twotheta_peaks.append(twotheta_peak)
    return twotheta_peaks


def get_idx(array_a, twoth):
    """
    Determine the index of 2theta which is nearest to given 2theta.

    Parameters
    ----------
    array_a : ndarray
        Numpy 2-dimensional array ([[2theta, intensity],
                                    [2theta, intensity],
                                    ...                ]).
    twoth : float
        Value of 2theta for which we want a (near) index.

    Returns
    -------
    idx : integer
        Index in array_a of the 2theta value which is nearest to the
        given twoth

    """
    twoth_axis = array_a[..., 0]    # Get the X axis (two theta) values
    # Subtract given twoth from each 2theta value in twoth_axis
    diff_2th = abs(twoth_axis - twoth)
    # idx is the index of the smallest item in diff_2th (= index of
    # 2theta closest to the given 2theta)
    idx = np.argmin(diff_2th)
    return idx


def test_latt_ct_cubic():
    d_test0 = latt_ct_cubic(1e-10, 60, (1, 0, 0))
    #test the calculation is correct
    assert d_test0 == pytest.approx(1)
    #test ValueError exception is raised if wavelength has unexpected value
    with pytest.raises(ValueError):
        latt_ct_cubic(1, 60, (1, 0, 0))

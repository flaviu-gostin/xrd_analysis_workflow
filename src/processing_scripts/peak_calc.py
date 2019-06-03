"""Calculate lattice spacing from peak position"""

import numpy as np
import pytest
import os
import natsort

wl = 0.6907e-10    # Wavelength in meter
roi_Pd113 = (33.5, 34.6)    # (start, end) values of 2theta interval of Pd113
location_stacks = "../../results/intermediate/integrated_1D/"

"""scans_patterns is a list giving the directories in location_stacks
where 1D patterns are, and patterns used for calculating the average
lattice spacing of Pd as a tuple (first pattern, last pattern + 1, step)"""
scans_patterns = [["PS_1p3V_b", (0, 82)],
                  ["PSA_1p3V_c", (0, 44)],
                  ["PSP_1p3V_b", (0, 63)],
                  ["PSAP_1p3V_a", (10, 31)],
                  ["PS_0p7V_b", (0, 69)],
                  ["PS_0p5V_b", (0, 119)],
                  ["PS_0p0V_a", (143, 148)],
                  ["PS_0p0V_a", (69, 74)],
                  ["PS_0p0V_a", (0, 5)]]

results_file = "../../results/final/table_Pd_summary.txt"


def spacing(wavelength, peak_pos):
    """
    Calculate spacing of cubic lattice from 113 peaks.
    
    Calculate the spacing of a cubic lattice from the position of the
    113 peak using Bragg's law and simple geometry.

    Parameters
    ----------
    wavelength : float
        The value of the wavelength in meter used to measure the
        diffraction pattern.
    peak_pos : float
        The position of the 113 diffraction peak in degree.

    Returns
    -------
    a : float
        Value of lattice spacing.

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
    # a is lattice spacing
    a = d * np.sqrt(1**2 + 1**2 + 3**2)
    return a


def peak_positions(dir_1D, patterns):
    """
    Determine the Pd113 peak positions for given patterns.

    For each pattern in given patterns determine the two-theta value of
    the highest intensity in the Pd113 region.

    Parameters
    ----------
    dir_1D : string
        Directory where the 1D diffraction pattern are
    patterns : tuple
        Tuple with 2 integers (first pattern, last pattern + 1)

    Returns
    -------
    out : list
        List containing two-theta values in degrees representing the
    maxima of Pd113 peaks.

    """
    # twotheta_peaks is a list collecting peak maxima
    twotheta_peaks = []
    # Determine array indices for roi_Pd113 from the first file in directory
    patt0 = np.loadtxt(dir_1D + str(patterns[0]) + ".dat",
                       usecols=(0,1))
    st, end = get_indices(patt0, roi_Pd113[0], roi_Pd113[1])
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

    
def get_indices(array_a, twoth_st, twoth_end):
    """ Determine the start and end indices of given 2theta interval 

    array_a: 2D array ([[2theta values list], [intensity values list]])
    (start, end): start and end 2theta values of given interval

    """

    twoth_axis = array_a[..., 0]    # Get the X axis (two theta) values
    diff_st = abs(twoth_axis - twoth_st)   # Subtract Pd113 start two theta value
    st_idx = np.argmin(diff_st)    # Index of roi_Pd113 start two theta 

    diff_end = abs(twoth_axis - twoth_end)
    end_idx = np.argmin(diff_end)

    return (st_idx, end_idx)


def latt_sp_avg(dir_1D, patterns, wl):
    """
    Calculate average lattice spacing of Pd.

    Calculates the average lattice spacing of Pd from the Pd113 peak for each 
    pattern and then calculates the average over all given patterns.

    Parameters
    ----------
    dir_1D : string
        Directory where the 1D diffraction pattern are
    patterns : tuple
        Tuple with 2 integers (first pattern, last pattern + 1)
    wl : float
        Wavelength in meter.

    Returns
    -------
    out : float
        Float number representing the average of the Pd lattice
    spacing.

    """ 

    latt_sp_sum = 0    # lattice spacing summed over all patterns
    for tth in peak_positions(dir_1D, patterns):
        latt_sp_sum += spacing(wl, tth)
    latt_sp_avg = latt_sp_sum / len(peak_positions(dir_1D, patterns))
    return latt_sp_avg


with open(results_file, "w") as rf:
    rf.write("# This is a summary table of lattice spacing values determined from the Pd113 peak \n")
    for [scan, patterns] in scans_patterns:
        dir_1D = location_stacks + scan + "/"
        lsa = latt_sp_avg(dir_1D, patterns, wl)
        #e is the electrolyte
        e = scan.split('_')[0]
        #p is the potential
        p = scan.split('_')[1]
        rf.write(e + "     " + p + "    " +
                 str(np.around(lsa, decimals=4)) + "\n")
    
    
def test_spacing():
    d_test0 = spacing(1e-10, 60)
    assert d_test0 == pytest.approx(1)
    with pytest.raises(ValueError):
        spacing(1, 60)

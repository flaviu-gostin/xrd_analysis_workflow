""" Calculate lattice spacing from peak position """

import numpy as np
import pytest
import os
import natsort


wl = 0.6907e-10    # Wavelength in meter
Pd113 = (33.5, 34.6)    # (start, end) values of 2theta interval of Pd111
loc_stack = "../../results/intermediate/integrated_1D/PS_1p3V_b/"
patterns = (0, 82)    # (first pattern, last pattern + 1, step)
results_file = "../../results/final/table_Pd_summary.txt"


def spacing(wavelength, two_theta):
    """ Calculate lattice spacing in Angstrom using Bragg's law and basic geometry
        
        wavelength: in meter
        two_theta: in degree

    """

    if wavelength < 1e-12 or wavelength > 1e-9:
        raise ValueError(str(wavelength) + " (meter) is an unlikely value for the wavelength")

    wl = wavelength * 1e+10    # Change unit to Angstrom
    theta = ((two_theta / 2) * np.pi ) / 180   # Calculate theta in radian
    d = wl / (2 * np.sin(theta))    # Bragg's law
    a = d * np.sqrt(1**2 + 1**2 + 3**2)    # Lattice spacing (a) from the interplanar distance (d) of Pd113 atomic planes

    return a


def peak_positions(loc_stack, patterns):
    """ Returns list of Pd113 peak positions for each pattern in a stack"""

    twotheta_peaks = []    # Defined as the 2theta value of the peak top

    # Determine array indices for Pd113 from the first file in directory 
    patt0 = np.loadtxt(loc_stack + str(patterns[0]) + ".dat", usecols=(0,1))
    st, end = get_indices(patt0, Pd113[0], Pd113[1])
    
    files = natsort.natsorted(os.listdir(loc_stack))[patterns[0]:patterns[1]]

    for file in files:
        pattern_whole = np.loadtxt(loc_stack + file, usecols=(0, 1))
        roi = pattern_whole[st:end, : ]    # Slice the Pd113 region
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
    st_idx = np.argmin(diff_st)    # Index of Pd113 start two theta 

    diff_end = abs(twoth_axis - twoth_end)
    end_idx = np.argmin(diff_end)

    return (st_idx, end_idx)



latt_sp_sum = 0    # lattice spacing summed over all patterns
for tth in peak_positions(loc_stack, patterns):
   latt_sp_sum += spacing(wl, tth)
latt_sp_avg = latt_sp_sum / len(peak_positions(loc_stack, patterns))


with open(results_file, "w") as rf:
    rf.write("# This is summary table of lattice spacing values determined from the Pd113 peak \n")
    rf.write("PS    1.3V    " + str(np.around(latt_sp_avg, decimals=4)))
    
    
def test_spacing():
    d_test0 = spacing(1e-10, 60)
    assert d_test0 == pytest.approx(1)
    with pytest.raises(ValueError):
        spacing(1, 60)
    
        
    

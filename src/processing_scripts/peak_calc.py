""" Calculate lattice spacing from peak position """

import numpy as np
import numpy.testing as npt
import pytest


# array = np.loadtxt(file, usecols=(0, 1)) # returns 2D array, each col is a list
# get a slice of array containing the Pd111 peak


# def peak_max(slice):
#     find max of second list in slice
#     find the corresponding value in first list
#     return 2theta value of peak max

Pd111 = (28.603, 29.404)    # (start, end) values of 2theta interval of Pd111


def spacing(wavelength, two_theta):
    """ Calculate lattice spacing in Angstrom using Bragg's law
        
        wavelength: in meter
        two_theta: in degree

    """

    if wavelength < 1e-12 or wavelength > 1e-9:
        raise ValueError(str(wavelength) + " (meter) is an unlikely value for the wavelength")

    wl = wavelength * 1e+10    # Change unit to Angstrom
    theta = ((two_theta / 2) * np.pi ) / 180   # Calculate theta in radian
    d = wl / (2 * np.sin(theta))
    return d



def peak_positions(directory):
    """ Returns list of peak position of Pd113 for each pattern in a stack"""
    peak_positions = []
    pattern0 = np.loadtxt(directory + "0.dat", usecols=(0,1))
    get_indices(pattern0, Pd111)

        for file in directory:
            pattern_whole = np.loadtxt(file, usecols=(0, 1))
            get the region of interest
            two_theta_max = two_theta of max intensity
            peak_positions.append

    return peak_positions

    
def get_indices(array_a, (start, end)):
    """ Determine the start and end indices of given 2theta interval 

    array_a: 2D array ([[2theta values list], [intensity values list]])
    (start, end): start and end 2theta values of given interval

    """
    
    i = 0
    while array[0, i] < start:
        i += 1
    start_index = i

    i = array.shape[-1]
    while array[0, i] > end:
        i -= 1
    end_index = i

    return (start_index, end_index)



def peak_max(sliced_array):
    

sliced_array = array[..., start_index:end_index]
find maximum in sliced_array[1]
return the corresponding value in sliced_array[0]
        
    a = peak_max(slice)
    
    
    


def test_spacing():
    d_test0 = spacing(1e-10, 60)
    npt.assert_almost_equal(d_test0, 1, decimal=7)
    with pytest.raises(ValueError):
        spacing(1, 60)
    
        
    

""" Test calculate_pattern function

Run from poject root: python -m pytest [src/tests/test_calculate_pattern.py]

"""
import numpy as np
from pymatgen import Structure
import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from calculate_pattern import calculate_pattern

peaks_file = os.path.join(os.path.dirname(__file__), "Si_peaks_NIST.txt")
cif_file = os.path.join(os.path.dirname(__file__), "Si.cif")
reference_peaks = np.loadtxt(peaks_file, delimiter=',', usecols=3)
lattice_param = 5.43118 # in Angstrom (Si powder SRM 640e from NIST)
wavelength = 1.5405929 # in Angstrom
two_theta_range = (0, 140) # in degree


def test_calculate_pattern():
    """ Test function calculate_pattern """
    structure = Structure.from_file(cif_file)

    # make the lattice parameter equal to the NIST one
    structure.scale_lattice(lattice_param ** 3)

    twotheta, intensity, _ = calculate_pattern(structure, wavelength,
                                            two_theta_range)
    np.testing.assert_allclose(twotheta, reference_peaks, rtol=0, atol=0.001)

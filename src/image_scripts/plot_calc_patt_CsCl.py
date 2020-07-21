""" This script plots a calculated diffraction pattern of CsCl.

This is for manual testing purposes.

"""
from pymatgen import Lattice, Structure
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from calculate_pattern import calculate_pattern, plot_calculated_pattern


wavelength = 1.0
two_theta_range = (0, 90)
# Create CsCl structure
a = 4.209 # in Angstrom
latt = Lattice.cubic(a)
structure = Structure(latt, ["Cs", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
two_th, intensity = calculate_pattern(structure, wavelength, two_theta_range)

plot_calculated_pattern(two_th, intensity)
plt.show()

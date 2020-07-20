""" This script plots a calculated diffraction pattern of CsCl.

This is for testing purposes.

"""
from pymatgen import Lattice, Structure
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
(two_th, intensity) = calculate_pattern(structure, wavelength, two_theta_range)

savefile = "plot_calc_CsCl-delete_me.png"
plot_calculated_pattern(two_th, intensity, 'blue', savefile)
print("File {} should have been created".format(savefile))
print("You may delete it")
print("The plot should also be shown in a window")

plot_calculated_pattern(two_th, intensity, 'blue')

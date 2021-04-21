""" Calculate X-ray diffraction peaks from a given structure

Usage: python calculate_pattern.py cif_file result_file [lattice_ct]

cif_file : CIF file for structure for which to calculate diffraction peaks
result_file : save peaks to this file
lattice_ct : change the lattice constant to this value in Angstrom (only makes
             sense for cubic systems)

"""

import numpy as np
from pymatgen import Structure
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from calculate_pattern import calculate_pattern
sys.path.append(os.path.join(os.path.dirname(__file__), "../../data/"))
from exper_param import wavelength


wavelength_Angstrom = wavelength * 1e10
two_theta_range = (0, 180)
cif_fname = sys.argv[1]
result_fname = sys.argv[2]
structure = Structure.from_file(cif_fname)

try:
    lattice_param = float(sys.argv[3])
    structure.scale_lattice(lattice_param ** 3)
except IndexError:
    pass

twotheta, intensity, hkl_labels = calculate_pattern(structure,
                                                    wavelength_Angstrom,
                                                    two_theta_range)
stacked_array = np.column_stack((twotheta, intensity, hkl_labels))
np.savetxt(result_fname, stacked_array, fmt = '%s')

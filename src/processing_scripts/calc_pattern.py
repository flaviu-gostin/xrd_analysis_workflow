""" Calculate X-ray diffraction peaks from a given structure

Usage: python calculate_pattern.py cif_file result_file

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
twotheta, intensity = calculate_pattern(structure, wavelength_Angstrom,
                                        two_theta_range)
stacked_array = np.column_stack((twotheta,intensity))
np.savetxt(result_fname, stacked_array, fmt='%.6e')

"""This script performs azimuthal integration.

It takes a hdf file and creates a 2theta-intensity dat file for each slice in
that hdf file using the refined geometry in a poni file.

Usage: python azimuthal_integration.py poni-file hdf-file results-dir

"""

import numpy as np
import pyFAI
import h5py
import sys


poni_file = sys.argv[1]
# create azimuthal integrator object
ai = pyFAI.load(poni_file)


hdf_filename = sys.argv[2]
# print("Integrating diffraction images in:", hdf_filename)
hdf_file = h5py.File(hdf_filename, 'r')
diffraction_images = hdf_file['entry/instrument/detector/data']

results_dir = sys.argv[3]
for idx, image in enumerate(diffraction_images):
    result_filename = results_dir + "/" + str(idx) + ".dat"
    ai.integrate1d(image, 4153, unit="2th_deg", filename=result_filename)

hdf_file.close()


# "image" would be "slice" in DAWN terminology (perhaps in hdf terminology too)

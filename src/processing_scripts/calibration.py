""" This script performs calibration of experiment geometry.

Usage: python calibration.py experiment-parameters-file poni-file

experiment-parameters-file : file from which to get experiment parameters
poni-file : file to write the calibration info to

"""


import numpy as np
import sys
import pyFAI
pyFAI.use_opencl = False    # It must be set before requesting any OpenCL modules

from pyFAI.calibrant import get_calibrant
from pyFAI.geometryRefinement import GeometryRefinement
import datetime

# import experiment-parameters-file as a module
import importlib
spec = importlib.util.spec_from_file_location('what.ever', sys.argv[1])
exper_param = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exper_param)


# Refined gemetry will be saved in this .poni file
poni_file = sys.argv[2]

# Experimental parameters
cal = get_calibrant(exper_param.calibrant)
cal.wavelength = exper_param.wavelength
det = pyFAI.detectors.Detector(exper_param.detector_pixel_size[0],
                               exper_param.detector_pixel_size[1])
det.max_shape = exper_param.detector_shape

# Approximate geometry to start with (to be refined by this script)
d = exper_param.distance_sample_detector
p1 = exper_param.poni1
p2 = exper_param.poni2
r1 = exper_param.rot1
r2 = exper_param.rot2
r3 = exper_param.rot3

# points on diffraction rings selected manually from the calibration image
pts = np.array(exper_param.p, dtype="float64")

geo_ref = GeometryRefinement(data=pts, dist=d, poni1=p1, poni2=p2, rot1=r1,
                             rot2=r2, rot3=r3, detector=det,
                             wavelength=exper_param.wavelength, calibrant=cal)


geo_ref.refine2()


# generate new .poni file
with open(poni_file, "w") as poni_f:
    poni_f.write("# Calibration done " + str(datetime.datetime.now()) + "\n")
    poni_f.write("PixelSize1: " + str(geo_ref.pixel1) + "\n")
    poni_f.write("PixelSize2: " + str(geo_ref.pixel2) + "\n")
    poni_f.write("Distance: " + str(geo_ref.dist) + "\n")
    poni_f.write("Poni1: " + str(geo_ref.poni1) + "\n")
    poni_f.write("Poni2: " + str(geo_ref.poni2) + "\n")
    poni_f.write("Rot1: " + str(geo_ref.rot1) + "\n")
    poni_f.write("Rot2: " + str(geo_ref.rot2) + "\n")
    poni_f.write("Rot3: " + str(geo_ref.rot3) + "\n")
    poni_f.write("Wavelength: " + str(geo_ref.wavelength) + "\n")

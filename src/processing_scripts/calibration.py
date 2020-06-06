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
d = 1.3e-1    # Distance sample to detector, measured with a ruler
p1 = 2e-3     # Estimated poni1
p2 = 2e-3
r1 = 0        # rot1
r2 = 0
r3 = 0

# Several points on each diffraction ring selected manually from the calibration
# diffraction image (Si_17.95keV)
p =[]
p.append([854, 21, 0])    # [dim0 (in pixels), dim1, ring index]
p.append([854, 86, 0])
p.append([950, 527, 0])
p.append([1045, 696, 0])
p.append([1217, 902, 0])
p.append([1654, 1155, 0])
p.append([2000, 1206, 0])
p.append([66, 66, 1])
p.append([66, 134, 1])
p.append([70, 186, 1])
p.append([321, 1017, 1])
p.append([499, 1278, 1])
p.append([1110, 1774, 1])
p.append([1193, 1814, 1])
p.append([1519, 1932, 1])
p.append([1837, 1987, 1])
p.append([1926, 1991, 1])
p.append([17, 1250, 2])
p.append([33, 1268, 2])
p.append([123, 1410, 2])
p.append([734, 1994, 2])
p.append([959, 2121, 2])
p.append([1775, 2357, 2])
p.append([1904, 2366, 2])
p.append([246, 2348, 3])
p.append([672, 2616, 3])
p.append([1943, 2943, 3])
p.append([141, 2676, 4])
p.append([712, 2998, 4])
p.append([2018, 3270, 4])
p.append([112, 3290, 5])
p.append([1010, 3666, 5])
p.append([1843, 3800, 5])
p.append([127, 3666, 6])
p.append([707, 3905, 6])
p.append([1431, 4081, 6])
pts = np.array(p, dtype="float64")


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

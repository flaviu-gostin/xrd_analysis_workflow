"""This script plots the diffraction image of our calibrant (Si) and overlays
a fake diffraction image calculated for our setup

"""


import pyFAI
pyFAI.use_opencl = False    # It must be set before requesting any OpenCL modules
from pyFAI.calibrant import get_calibrant
import matplotlib.pyplot as plt


# The .poni file containing the refined geometry parameters
poni_file = "../../results/intermediate/calibration/Si_17950eV.poni"

cal = get_calibrant("Si")
detector_shape = (2045, 4096) 


ai = pyFAI.load(poni_file)
img = cal.fake_calibration_image(ai, shape=detector_shape)


plt.imshow(img)
plt.show()

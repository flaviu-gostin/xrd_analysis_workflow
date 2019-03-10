""" Open a window with the raw diffraction image of Si"""


import matplotlib.pyplot as plt
import sys


location_of_data = "../../data/calibrant_Si/"
filename1 = "Si_17.95keV.hdf"
file1 = location_of_data + filename1

location_of_functions = "../functions/"

sys.path.append(location_of_functions)

from get_slice import get_slice


slc = get_slice(file1, 0)
plt.imshow(slc)
plt.title(file1 + ", slice no 0")

plt.show()

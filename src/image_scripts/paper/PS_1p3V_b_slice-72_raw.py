""" Creates raw diffraction images for the manuscript """

import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),
                             "../../functions/"))
from hdf_view import get_slice
sys.path.append(os.path.join(os.path.dirname(__file__),
                             "../../../data/"))
import inside_hdf

dataset_path = inside_hdf.hdf_dataset_path
location_of_data = "../../../data/"
location_of_images = "../../../results/final/"
condition = "PS_1p3V_b"
slice = 72

file = location_of_data + condition + ".hdf"
slc = get_slice(file, dataset_path, slice)
plt.imshow(slc, cmap='gray_r', vmin=2000, vmax=15000)
plt.xticks(())
plt.yticks(())
save_filename = condition + "_slice-" + str(slice) + "_raw.png"
plt.savefig(location_of_images + save_filename, dpi=500)
plt.close()

"""Creates raw diffraction images for the manuscript"""


import matplotlib.pyplot as plt
import sys
location_of_functions = "../functions/"
sys.path.append(location_of_functions)
from get_slice import get_slice


location_of_data = "../../data/"
location_of_images = "../../results/final/"
slices_to_plot = [("PS_1p3V", 71)]    # [(file, slice no), ...]


for (condition, slice) in slices_to_plot:
    file = location_of_data + condition + ".hdf"
    slc = get_slice(file, slice)
    plt.imshow(slc, cmap="gray")
    plt.xticks(())
    plt.yticks(())
    plt.title(condition + ", slice " +  str(slice))
    save_filename = condition + "_slice-" + str(slice) + "_raw.png"
    plt.savefig(location_of_images + save_filename, dpi=500)
    plt.close()

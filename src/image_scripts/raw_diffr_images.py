"""Creates raw diffraction image"""

print("Generating raw diffraction images ...")

import matplotlib.pyplot as plt
import sys


location_of_data = "../../data/"
location_of_images = "../../images/"
filename1 = "cmos-72532_FOR_TESTS.hdf"
file1 = location_of_data + filename1
# filename2 = ...
# file2 = ...
slices_to_plot = [(file1, 71),
                  (file1, 72)]    # [(file, slice no), ...]
location_of_functions = "../functions/"


sys.path.append(location_of_functions)

from get_slice import get_slice


for (file, slice) in slices_to_plot:
    slc = get_slice(file, slice)
    plt.imshow(slc, cmap="gray")
    plt.xticks(())
    plt.yticks(())
    plt.title(file + ", slice " +  str(slice))
    filename = file.split("/")[-1]
    file_no = filename[5:10]
    save_file = file_no + "_" + str(slice) + "_raw.png"
    plt.savefig(location_of_images + save_file)
    plt.close()
    print("Saved", save_file)

print("Done")

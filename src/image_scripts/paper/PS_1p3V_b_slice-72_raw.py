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
fig, ax = plt.subplots(subplot_kw={'autoscale_on': True})
ax.imshow(slc, cmap='gray_r', vmin=2000, vmax=15000)
plt.xticks(())
plt.yticks(())

#annotations
y_ann = 2044
y_offset = -25
labels = [['CuCl 111', 1209, 'green'],
          ['Pd 111', 1692, 'blue'],
          ['CuCl 022', 1995, 'green'],
          ['CuCl 113', 2374, 'green'],
          ['Pd 022', 2904, 'blue'],
          ['Pd 113', 3522, 'blue']
          ]
for label, x_ann, color in labels:
    ax.annotate(label, xy=(x_ann,y_ann), xycoords='data',
                xytext=(0, y_offset), textcoords='offset points',
                color=color, fontsize=16,
                rotation=90, ha='center', va='top',
                arrowprops=dict(arrowstyle="->",
                                color=color)
                )

save_filename = condition + "_slice-" + str(slice) + "_raw.png"
fig.savefig(location_of_images + save_filename, dpi=500)
plt.close()

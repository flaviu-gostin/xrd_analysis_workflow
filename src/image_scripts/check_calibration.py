""" Create one image and one plot to manually check the calibration.

The image and the plot are saved in the results directory.

"""
import pyFAI
pyFAI.use_opencl = False    # It must be set before requesting any OpenCL modules
from pyFAI.calibrant import get_calibrant
import numpy as np
import matplotlib.pyplot as plt
from pymatgen import Structure
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
from hdf_view import get_slice
from calculate_pattern import calculate_pattern, plot_calculated_pattern
sys.path.append(os.path.join(os.path.dirname(__file__), "../../data/"))
import inside_hdf, exper_param

dataset_path = inside_hdf.hdf_dataset_path
Si_hdf_file = "../../data/Si_17.95keV.hdf"
slice = 0
Si_1D_file = "../../results/intermediate/integrated_1D/Si_17.95keV/0.dat"
Si_cif_file = "../../data/cif/Si.cif"
Si_lattice_param = 5.43118 # in Angstrom (Si powder SRM 640e from NIST)
poni_file = "../../results/intermediate/Si_17.95keV.poni"
measured_image = get_slice(Si_hdf_file, dataset_path, slice)
image_fn = "../../results/intermediate/check_calibration_image.png"
pattern_fn = "../../results/intermediate/check_calibration_pattern.png"

cal = get_calibrant("Si")
detector_shape = (2045, 4096)
ai = pyFAI.load(poni_file)
fake_image = cal.fake_calibration_image(ai, shape=detector_shape)

pattern_1D = np.loadtxt(Si_1D_file)

structure_Si = Structure.from_file(Si_cif_file)
# make the lattice parameter equal to the NIST one
structure_Si.scale_lattice(Si_lattice_param ** 3)
wl = exper_param.wavelength * 1e10
twotheta, intensity, *_ = calculate_pattern(structure_Si, wl, (0, 41.6))


title = """Two superimposed images: measured image and "fake" image"""
plt.imshow(measured_image, cmap='binary')
plt.title(title)
plt.imshow(fake_image, cmap='summer', alpha=0.7)
plt.savefig(image_fn, dpi=500)
plt.close()


plt.plot(pattern_1D[:,0], pattern_1D[:,1], linewidth=0.5)
stem_container = plt.stem(twotheta, intensity * 200)
stem_container.baseline.set_visible(False)
stem_container.markerline.set_visible(False)
stem_container.stemlines.set_linewidth(0.5)
stem_container.stemlines.set_color("green")
plt.savefig(pattern_fn, dpi=500)
plt.close()

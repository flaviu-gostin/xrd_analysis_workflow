"""Make copies of all hdf files with only the first two slices

Usage: python3 generate_mock_hdf_files.py orig-filename output-filename

orig-filename : filename of original hdf file

output-filename : filename of mock hdf file containing the first 2 slices in the
original file

Note: at the moment the attributes of groups and dataset are not copied as they
are not needed in the mock file for its foreseeable uses.

"""
import h5py
import sys

orig_filename = sys.argv[1]
output_filename = sys.argv[2]

#hdf files cannot be modified, so I will copy the modified dataset to a new file

orig_file = h5py.File(orig_filename, 'r')
# >>> orig_file
# <HDF5 file "PS_1p3V_b.hdf" (mode r)>
# >>> type(orig_file)
# h5py._hl.files.File

# http://docs.h5py.org/en/2.9.0/quick.html#core-concepts
orig_dataset = orig_file['entry/instrument/detector/data']
# >>> orig_dataset
# <HDF5 dataset "data": shape (101, 2045, 4098), type "<u2">
# >>> type(orig_dataset)
# h5py._hl.dataset.Dataset

# I want only the first 2 of those 101 diffraction images
slice_orig_dataset = orig_dataset[:2]
# Slicing results in a numpy array!
# >>> type(slice_orig_dataset), slice_orig_dataset.dtype
# (numpy.ndarray, dtype('uint16'))
orig_file.close()

output_file = h5py.File(output_filename, 'w')

# Recreate path to dataset
new_group = output_file.create_group('entry/instrument/detector')
# Create new dataset with the same name as in the original file, i.e. "data"
new_group.create_dataset('data', data=slice_orig_dataset)
# <HDF5 dataset "data": shape (2, 2045, 4098), type "<u2">
output_file.close()

# TO DO: output_file is larger than it should be.  It is 32M, should be 26M.
# Perhaps the original hdf files use compression? Or the max size is exact?

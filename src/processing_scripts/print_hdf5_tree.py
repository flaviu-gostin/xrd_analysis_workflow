"""
Print the entire hierarchy of a hdf5 file.

Run with: python print_hdf5_tree.py FILENAME

FILENAME can be abcd.hdf or abcd.nxs

"""

import h5py
import sys

def print_hdf5_tree(fname):
    """Print the entire hierarchy of a hdf5 file.

    Note (May 2016):
    Data from the diffraction detector at beamline I18 (Diamond, UK)
    comes in files with extension 'hdf', but most metadata is in
    complementary files with extension 'nxs'.  To get that metadata, run
    this function on the 'nxs' file.

    """
    def find_all(name, object):
        """ What to print for each member of the tree """

        if isinstance(object, h5py.Dataset):
            if object.shape == (1,):
                print('Dataset named: ', name, '(value =', object[()], ')')
            else:
                print('Dataset named: ', name, '(shape:', object.shape,
                      ', type:', object.dtype, ')')
        elif isinstance(object, h5py.Group):
            print('+ Group named: ', name)
            for item in object.attrs.items():
                print('Attribute: ', item)

    file = h5py.File(fname, 'r')
    file.visititems(find_all)
    file.close()


if __name__ == "__main__":
    print_hdf5_tree(sys.argv[1])

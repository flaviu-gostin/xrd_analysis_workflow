"""
Print the entire hierarchy of a hdf5 file.

Run with: python print_hdf5_tree.py FILENAME

FILENAME can be abcd.hdf or abcd.nxs

"""

import h5py
import sys


file = h5py.File(sys.argv[1], 'r')

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


file.visititems(find_all)


file.close()

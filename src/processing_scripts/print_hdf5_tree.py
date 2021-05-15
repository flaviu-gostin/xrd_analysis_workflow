"""
Print the entire hierarchy of a hdf5 file

Run with: python print_hdf5_tree.py FILENAME

"""


import h5py
import sys


# Open the hdf5 file
file = h5py.File(sys.argv[1], 'r')


def find_all(name, object):
    """ What to print for each member of the tree """

    if isinstance(object, h5py.Dataset):    # if the member is a Dataset ...
        if object.shape == (1,):    # has one dimension with one single value
            print(name, '(Dataset, value =', object[()], ')')    # print value
        else:
            print(name, '(Dataset, shape:', object.shape, ', type:', object.dtype, ')')    # otherwise print the shape and type

    elif isinstance(object, h5py.Group):
        print(name, '(Group)')


file.visititems(find_all)


file.close()

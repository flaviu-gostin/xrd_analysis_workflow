"""Get all sorts of data from hdf5 files.

Get tree info (the structure of the hdf5 file).
Get actual data sets contained inside the file.

Use: from hdf_view import the_function_you_need

https://docs.h5py.org/en/stable/high/group.html

"""
import h5py

def get_slice(filename, dataset_path, n):
    """Extract one single slice from a .hdf file.  Counting starts at 0."""
    file = h5py.File(filename, 'r')
    dataset = file[dataset_path]
    slice = dataset[n]
    file.close()
    return slice


def print_tree(fname):
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

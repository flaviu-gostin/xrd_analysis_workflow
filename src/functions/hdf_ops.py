"""Get all sorts of data from hdf5 files.

Get tree info (the structure of the hdf5 file).
Get actual data sets contained inside the file.

Use: from hdf_ops import the_function_you_need

https://docs.h5py.org/en/stable/high/group.html

"""
import h5py

def get_diffraction_image(fname, dataset_path, n):
    """Extract one diffraction image from a .hdf file.

    Counting starts at 0.

    Image is equivalent to 'slice' in DAWN software.

    """
    file = h5py.File(fname, 'r')
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


def vertical_position(fname, images_idx=None):
    """Get vertical position for diffraction images from nxs file.

    Arguments
    ---------
    fname (string): Name of hdf5 file containing the metadata (.nxs).

    images_idx (list or int): List of indices for diffraction images
        (slices) for which to get the vertical position at which they
        were captured.  If None, return position for all images.

    Returns
    -------
    (list of floats): List of vertical positions.

    FORMAT THIS DOCSTRING PROPERLY!

    """
    file = h5py.File(fname, 'r')
    scan_command_dataset = file["entry1/scan_command"]
    scan_command_str = scan_command_dataset[0]
    images_no_dataset = file["entry1/scan_dimensions"]
    images_no = images_no_dataset[0]
    file.close()
    sc_split = scan_command_str.split()
    pos_0 = float(sc_split[2])
    step = float(sc_split[4])
    max_idx = images_no - 1

    if not images_idx:
        images_idx = range(images_no)


    if isinstance(images_idx, int):
        if 0 <= images_idx <= max_idx:
            return pos_0 + images_idx*step
        else:
            raise ValueError("Image index {} is out of range".format(\
                                                            images_idx))


    if all(0 <= idx <= max_idx for idx in images_idx):
        positions = [round(pos_0 + idx*step, 3) for idx in images_idx]
    else:
        raise ValueError("One or more image indices are out of range")

    return positions

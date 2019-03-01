"""
Print the entire hierarchy of a hdf5 file

Run with: python print_hdf5_hierarchy.py

"""


import h5py


def print_hdf5_hierarchy(file_name):
    """Print the entire hierarchy of a hdf5 file"""
    file = h5py.File(file_name, 'r')
    print(file.name)

#    offset = '    '
#    i = 1
    def print_members(group):
        for m in group.__iter__():
            print(m)
            if isinstance(group[m], h5py.Group):
                print('    ', print_members(group[m]))
                
    print_members(file)
    
    file.close()

    
print_hdf5_hierarchy('../../data/cmos-72532_FOR_TESTS.hdf')


#def test_print_hdf5_structure:
#    struct = print_hdf5_structure()

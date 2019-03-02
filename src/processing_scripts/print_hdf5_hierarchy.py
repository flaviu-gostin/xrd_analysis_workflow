"""
Print the entire hierarchy of a hdf5 file

Run with: python print_hdf5_hierarchy.py FILENAME

"""


import h5py
import sys


def print_hdf5_hierarchy(file_name):
    """Print the entire hierarchy of a hdf5 file"""
    file = h5py.File(file_name, 'r')
    print(file.name)

    def print_members(group, level):
        for m in group.__iter__():
            if isinstance(group[m], h5py.Group):
                print('{0}{1}{2}{1}'.format('    ' * level, '/', m))
                level += 1
                print_members(group[m], level)
            else:
                print('{0}{1}{2}'.format('    ' * level, '/', m))
                
    print_members(file, 0)
    
    file.close()

    
print_hdf5_hierarchy(sys.argv[1])


#def test_print_hdf5_structure:
#    struct = print_hdf5_structure()

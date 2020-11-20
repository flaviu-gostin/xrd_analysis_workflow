# The data/ directory

The data/ directory contains only raw data (processed data is located
in the [results/](results/) directory).  Because the raw data is
large, it is stored separately in a [data repository on
Zenodo](https://zenodo.org/record/4039843).  For each dataset there
are two files and a directory, e.g. PS_1p3V_b.hdf, PS_1p3V_b.nxs and
PS_1p3V_b/.  Both files are HDF5 files.  The *.hdf files contain the
actual stack of 2D diffraction images.  The *.nxs files contain
beamline setup parameters and some identifiers.  The corresponding
directories contain electrochemical data and camera photos associated
with the artificial pit samples used for the synchrotron X-ray
diffraction experiments.

**Recipes:**
- `make data` downloads data from Zenodo, concatenates split files,
  decompresses archives
- `make validate` checks md5 sums for each file
- `make clean-data` deletes split files and archives (does not delete
  the data required for data analysis).

**Filenames explained:**

* PS: physiological saline, which is a solution 0.9% NaCl
* PSA: PS + 4% albumin
* PSP: PS + 0.1% H2O2
* PSAP: PS + 4% albumin + 0.1% H2O2

* 1p3V: 1.3 V (applied potential of 1.3 V)

* Si_17.95keV: silicon calibrant at energy 17.95 keV

Most of the **electrochemical data** is in idf files (measured with
potentiostats from ©IVIUM Technologies, Netherlands), which can be
opened with a text editor, but mind the encoding (try ISO-8859-1).

# Data for tests

For testing purposes, two hdf files have been created (see directory
'test_data').  These two files contain only two diffraction images
each, to keep them small.  The two images are copies of the first two
images in the raw files with corresponding names.

To automatically re-generate the test files: `make test-data`

# The data/ directory

The data/ directory contains only raw data (processed data is located in the results/ directory).  Because the raw data is large, it is stored separately on (Zenodo, not yet really).  For each dataset there are two files, e.g. PS_1p3V_b.hdf and PS_1p3V_b.nxs.  Both are HDF5 files.  The *.hdf files contain the actual stack of two-dimensional diffraction images.  The *.nxs files contain beamline setup parameters and some identifiers.


Filenames explained:

* PS: physiological saline, which is a solution 0.9% NaCl
* PSA: PS + 4% albumin
* PSP: PS + ... peroxide
* PSAP:

* 1p3V: 1.3 V (applied potential of 1.3 V)
* 0p7V
* 0p5V
* 0V

* Si_17.95keV: silicon calibrant at energy 17.95 keV
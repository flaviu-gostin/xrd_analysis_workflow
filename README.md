# Data analysis for article Gostin et al 2018

P. F. Gostin et al., *In Situ Synchrotron X‐Ray Diffraction
Characterization of Corrosion Products of a Ti‐Based Metallic Glass
for Implant Applications*, Advanced Healthcare Materials, 2018, 7,
1800338 (<https://doi.org/10.1002/adhm.201800338>)

Free pre-publication full-text version:
[doc/manuscript_Gostin_2018.pdf](doc/manuscript_Gostin_2018.pdf)

**This project automatically:**
- downloads raw data from a [data repository on
  Zenodo](https://zenodo.org/record/4039843)
- processes the data (calibration, azimuthal integration etc.)
- plots figures and table

**To repeat the analysis**
- `git clone https://github.com/flaviu-gostin/xrd_analysis_workflow.git`
- `cd xrd_analysis_workflow/`
- `sudo apt install virtualenv`
- `python3 -m venv ./venv` You need Python3.8 for this project
- `source venv/bin/activate`
- `python3 -m pip install -r requirements.txt`
- `make all` Downloads 14.6 GB (but reserve 30 GB) and performs all
  the data processing and plotting.

You need to reserve more storage space as downloaded archives and
split files will automatically be decompressed/concatenated.  To
delete the archives and split files:
- `make clean-data`

You should find the results in [results/](results/)

## Questions and feedback

Please feel free to create an issue or a pull request on GitHub or
email me.

## How it works
- download raw 2D XRD image data from [a Zenodo
  repository](https://zenodo.org/record/4039843)
- perform azimuthal integration on those images resulting in 1D XRD
  patterns using [pyFAI](https://github.com/silx-kit/pyFAI)
- determine peak position, calculate lattice spacing and write values
  in a table
- calculate diffraction patterns from structures using
  [pymatgen](https://github.com/materialsproject/pymatgen)
- plot measured and calculated diffraction patterns using
  [matplotlib](https://github.com/matplotlib/matplotlib)

## Note on calibration (geometry refinement)

Calibration uses the Python module pyFAI.  This is listed in
requirements.txt.  When installing this module, a set of command line
interfaces (CLIs) are also installed in bin/, e.g. pyFAI-calib.  The
recommended way to do the calibration is to use the pyFAI-calib CLI
(there is also a GUI available for that).  With those interfaces the
user must click on several diffraction rings to help the program
locate the rings.  Another reason for using the CLI or the GUI is to
be able to check visually that the refined rings match well enough the
real rings of the calibrant.  However, I intentionally avoided using
either interface because clicks cannot be reproduced easily.  Instead,
I wrote a script which uses the refinement function in pyFAI and takes
as arguments a long list of manually selected points.  Thus, the
calibration is guaranteed to be reproducible.  Moreover, one can check
that the manually selected points are located on diffraction rings.

The refined (calibrated) geometry is saved in a .poni file.  This .poni file is
the basis for the azimuthal integrator object used to integrate all the
diffraction images.  Thus, if the calibration is changed, most of the results
might change.  This will most likely be a minor change.

# Data analysis for article Gostin et al 2018

P. F. Gostin et al., *In Situ Synchrotron X‐Ray Diffraction Characterization of
Corrosion Products of a Ti‐Based Metallic Glass for Implant Applications*,
Advanced Healthcare Materials, 2018, 7, 1800338
(<https://doi.org/10.1002/adhm.201800338>)

Free pre-publication version:
[doc/manuscript_Gostin_2018.pdf](doc/manuscript_Gostin_2018.pdf)

**This repo contains** Python code which performs data analysis, plots figures and
creates tables for the article mentioned above.

**How it works.**  In short:
- download the raw 2D XRD image data from a public data repository (only one set
  of images for now)
- perform azimuthal integration on those images resulting in 1D XRD patterns
  using [pyFAI](https://github.com/silx-kit/pyFAI)
- determine peak position, calculate lattice spacing and write values in a table
- calculate diffraction patterns from structures using
  [pymatgen](https://github.com/materialsproject/pymatgen)
- plot measured and calculated diffraction patterns using
  [matplotlib](https://github.com/matplotlib/matplotlib)

**This repo is for** people interested in knowing whether the results of the
data analysis are reproducible.  It is also for people who want to re-use some
of this code.

2020-05-08: This project is under work.  At the moment, it generates figures 1c
and S1 (in Supporting Information) and Table 2.  See
[results/final/](results/final/).

## To repeat the analysis, follow these steps:

### Clone this repository

- Open Terminal
- `cd Desktop`
- `git clone https://github.com/flaviu-gostin/xrd_analysis_workflow.git`

### Install required packages

It is recommended installing packages in a virtual environment as their versions
might be different from the ones you have on your system. For example:
- `cd xrd_analysis_workflow/`
- `sudo apt install virtualenv`
- `virtualenv --python=python3 venv` (this will create a directory named
  `venv/`, where required Python packages will be installed).  Note: this project
  requires Python>=3.6, because an important dependency pymatgen requires that.

To install required packages:
- `source venv/bin/activate` (if you want packages installed in the virtual
  environment)
- `pip install -r requirements.txt` (install all required Python packages with
  given versions)

### Download raw data and do the analysis

- `make all` (this will download an archive of 1.3 GB, and un-archive it (so you
  need >1.3GB free space on your drive), followed by analysis, which took
  approx. 2 min on an average laptop)

You should find the results (figures and tables) in [results/](results/)

## Feedback

Please let me know how it went by creating an issue at the top of the screen or
email me.  You are also welcome to send me pull requests.

## Note on calibration (geometry refinement)

Calibration uses the Python module pyFAI.  This is listed in requirements.txt.
When installing this module, a set of command line interfaces (CLIs) are also
installed in bin/, e.g. pyFAI-calib.  The recommended way to do the calibration
is to use the pyFAI-calib CLI (there is also a GUI available for that).  With
those interfaces the user must click on several diffraction rings to help the
program locatie of the rings.  Another reason for using the CLI or the GUI is to
be able to check visually that the refined rings match well enough the real
rings of the calibrant.  However, I intentionally avoided using either interface
because clicks cannot be reproduced easily.  Instead, I wrote a script which
uses the refinement function in pyFAI and takes as arguments a long list of
manually selected points.  Thus, the calibration is guaranteed to be
reproducible.  Moreover, one can check that the manually selected points are
located on diffraction rings.

The refined (calibrated) geometry is saved in a .poni file.  This .poni file is
the basis for the azimuthal integrator object used to integrate all the
diffraction images.  Thus, if the calibration is changed, most of the results
might change.  This will most likely be a minor change.

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

2020-05-08: This project is under work.  At the moment, it generates
figures 1c and S1 (in Supporting Information) and Table 2.  See [final
results](results/final/).

## To repeat the analysis, follow these steps:

### Clone this repository

- Open Terminal
- `cd Desktop`
- `git clone https://github.com/flaviu-gostin/xrd_analysis_workflow.git`

### Create a virtual environment and install required packages

For example:
- `cd xrd_analysis_workflow/`
- `sudo apt install virtualenv`
- `virtualenv --python=python3 venv` (this will create a directory named
  `venv/`, where required Python packages will be installed).  Note: this project
  was developed with Python3.5
- `source venv/bin/activate` (it can be deactivated with `deactivate`, but don't
  do it now)
- `pip install -r requirements.txt` (install all required Python packages)
- `make patch` (apply a patch which adds a try statement to
  azimuthalIntegrator.py, a pyFAI module, to circumvent an ImportError.  Without
  this patch, the analysis will not work.  See file
  xrd_analysis_workflow/azimuthalIntegrator.patch)

### Download raw data and do the analysis

- `make all` (this will download an archive of 1.3 GB, and un-archive it (so you
  need >1.3GB free space on your drive), followed by analysis, which took
  approx. 2 min on an average laptop)

You should find the results (figures and tables) in the directory
[results/](results/)

Note: if you get some ImportError warnings, you probably need to install those
 modules that are indicated in the warnings. Make sure the virtual environment
 is active and install those modules with `pip install module_name`. Then try
 again the command: `make all` or just `make analysis` if the raw data has
 already been downloaded.

## Feedback

Please let me know how it went by creating an issue at the top of the screen or
email me.  You are also welcome to send me pull requests.

# Analysis of 2D X-ray diffraction images

This workflow takes raw 2D images, performs azimuthal integration on them
resulting in an intensity versus 2theta plot and calculates lattice spacing from
peak position.

Please try to reproduce my results on your machine by following the steps
bellow.  You will know it worked if you get two figures and a text file in
`xrd_analysis_workflow/results/final/`.  These should look like Fig. 1c (page
25), Fig. S1 (page 35) and the 1st row in Table 2 (page 31) in the manuscript at
`xrd_analysis_workflow/doc/manuscript.pdf`.  Please let me know how it went by
issuing an `Issue` at the top of the screen or email me.  You are also welcome
to send me `Pull requests`.

## Follow these steps:

- Open the terminal
- Change directory to where you want to have the directory of this repository,
  e.g. Desktop, so `cd Desktop`
- Clone the repository with: `git clone
  https://github.com/craicrai/xrd_analysis_workflow.git`
- Change directory to the repository directory: `cd xrd_analysis_workflow/`
- Create a virtual environment, e.g. install virtualenv with `sudo apt install
  virtualenv` if it is not already installed and create a virtual environment
  with `virtualenv --python=python3 venv`.  This will create a directory named
  `venv/`, which will contain the Python packages.  The python3 version in your
  virtual environment will be the one in your system, in my case it was
  python3.5.
- Activate the virtual environment with `source venv/bin/activate` (you can
  deactivate it with `deactivate`, but don't do it now)
- Install the requirements in `requirements.txt`, e.g. with `pip install -r
  requirements.txt`
- Apply a patch with `make patch`. This adds a try statement to
  azimuthalIntegrator.py, a pyFAI module, to circumvent an ImportError.  Without
  this patch, the analysis will not work.  See file
  xrd_analysis_workflow/azimuthalIntegrator.patch
- Finally, download the raw diffraction data from Figshare and do the analysis
  simply with the command (make sure you are in the project root,
  i.e. `xrd_analysis_workflow` and the virtual environment is active): `make
  all`. This will download an archive of 1.3G in `data/`, and un-archive it (so
  it will write another 1.3G on your drive), followed by analysis, which took
  approx. 2 min on my laptop.
- If you get some ImportError warnings, you probably need to install those
  modules that are indicated in the warnings. Make sure the virtual environment
  is active and install those modules with `pip install module_name`. Then try
  again the command: `make all` or just `make analysis` if the raw data has
  already been downloaded at the previous `make all` (check the terminal output
  or the directory `xrd_analysis_workflow`)
- Finally finally, compare the files in `xrd_analysis_workflow/results/final/`
  directory with the manuscript as said above.

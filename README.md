# Analysis of 2D X-ray diffraction images

This workflow takes raw 2D images, performs azimuthal integration on them resulting in an intensity versus 2theta plot and calculates lattice spacing from peak position.

Please try to reproduce my results on your machine by following the steps bellow.  You will know it worked if you get two figures and a text file in `xrd_analysis_workflow/results/final/`.  These should look like Fig. 1c (page 25), Fig. S1 (page 35) and the 1st row in Table 2 (page 31) in the manuscript at `xrd_analysis_workflow/doc/manuscript.pdf`.  Please let me know how it went by issuing an `Issue` at the top of the screen or otherwise.  You are also welcome to send me `Pull requests`. 

## Follow these steps:

- Fork this repository. Click on the "Fork" button just below the top right of the screen
- Select the URL of your new forked repository from the URL bar, and copy it. The URL will be of form https://github.com/your-user-name/xrd_analysis_workflow
- Open the terminal
- Change directory to where you want to have the directory of this repository, e.g. Desktop, so `cd Desktop`
- Clone the repository with: `git clone [URL copied above]`
- Change directory to the repository directory: `cd xrd_analysis_workflow/`
- Create a virtual environment, e.g. install virtualenv with `sudo apt install virtualenv` if it is not already installed, create a virtual environment with `virtualenv --python=python3.5 venv` (a directory `venv/` will be created, which will contain the Python packages)
- Activate the virtual environment with `source venv/bin/activate` (you can deactivate it with `deactivate`, but don't do it now) 
- Install the requirements in `requirements.txt`, e.g. with `pip install -r requirements.txt`
- Dig deep inside the virtual environment directory for the module pyFAI.azimuthalIntegrator (something like `xrd_analysis_workflow/venv/lib/python3.5/site-packages/pyFAI/azimuthalIntegrator.py) and insert `try:` above `from .opencl import ocl`, of course indent the latter, and below it add two lines `except ImportError:` and with indent `ocl = None` (see Important note below)
- Finally, download the raw diffraction data from Figshare and do the analysis simply with the command (make sure you are in the project root, i.e. `xrd_analysis_workflow` and the virtual environment is active): `make all`
- If you get some ImportError warnings, you probably need to install those modules that are indicated in the warnings. Make sure the virtual environment is active and install those modules with `pip install module_name`
- Try again the command: `make all` or just `make analysis` if the raw data has been downloaded at the previous `make all` (check the terminal output or the directory `xrd_analysis_workflow`)
- Finally finally, compare the files in `xrd_analysis_workflow/results/final/` directory with the manuscript as said above.


## Important note

Unfortunately, when _from pyFAI.azimuthalIntegrator import AzimuthalIntegrator_ an _ImportError: cannot import name 'ocl'_ is raised with pyFAI 0.17.0. The solution that seems best now is to modify the pyFAI/azimuthalIntegrator.py module to add a `try` statement before the problematic import at line 178, as has been done for the latest version of that module on https://github.com/silx-kit/pyFAI/blob/master/pyFAI/azimuthalIntegrator.py, see commit 1e2b476

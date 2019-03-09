# Analysis of 2D X-ray diffraction images

This workflow takes raw 2D images, performs azimuthal integration on them resulting in an intensity versus 2theta plot.

(Unfortunately, when _from pyFAI.azimuthalIntegrator import AzimuthalIntegrator_ an _ImportError: cannot import name 'ocl'_ is raised with pyFAI 0.17.0. The solution that seems best now is to modify the pyFAI/azimuthalIntegrator.py module to add a try statement before the problematic import at line 178, as has been done for the latest version of that module on https://github.com/silx-kit/pyFAI/blob/master/pyFAI/azimuthalIntegrator.py, see commit 1e2b476)

## Follow these steps

### Step 1
"""Test rules in Makefiles using small test files

Note: Running this script will (might?) delete some result files.  It runs `make
clean-test` in a subprocess.

"""

import subprocess as sp
import os

hdf_stems = ['test-PS_1p3V_b', 'test-PSP_1p3V_b']
interm_dir = 'results/intermediate'
final_dir = 'results/final'
poni_file = os.path.join(interm_dir, 'Si_17.95keV.poni')
# not compliant with DRY: this variable is also defined in Makefile
# same for the next variables
integrated_1D_dir = os.path.join(interm_dir, 'integrated_1D')
integrated_1D_files = []
for hdf_stem in hdf_stems:
    for slice in ['0.dat', '1.dat']:
        integrated_1D_files.append(os.path.join(integrated_1D_dir, hdf_stem,
                                                slice))
peaks_dir = os.path.join(interm_dir, 'peaks')
peaks_files = [os.path.join(peaks_dir, hdf_stem + '_Pd113.dat') for hdf_stem in
               hdf_stems]
table_Pd_file = os.path.join(final_dir, 'table_Pd_summary.txt')


def make_rules():
    sp.run(['make', 'clean-test'])
    sp.run(['make', 'test'])


def test_make_rules():
    make_rules()
    assert os.path.exists(poni_file)
    for integrated_1D_file in integrated_1D_files:
        assert os.path.exists(integrated_1D_file)
    for peaks_file in peaks_files:
        assert os.path.exists(peaks_file)
    assert os.path.exists(table_Pd_file)
    sp.run(['make', 'clean-test'])

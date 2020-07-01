"""Determine peak position and lattice constant for series of patterns.

Usage: python3 determine_peak_position.py source-dir config-file
experiment-parameters-file output-file

A peak position value and a corresponding lattice constant value will be
determined for each file in 'source-dir'.  These values will be prefixed with
the source file basename and written to 'output-file'.  The source file basename
must consist of integers only, e.g. '0.dat' or '23.dat'.

"""
import numpy as np
import os
from collections import OrderedDict
import sys
#workaround to be able to append "functions" irrespective of cwd
script_abspath = os.path.abspath(sys.argv[0])
common_path = os.path.dirname(os.path.dirname(script_abspath))
sys.path.append(os.path.join(common_path, 'functions'))
from peak_calc import peak_position, latt_ct_cubic

import importlib
spec = importlib.util.spec_from_file_location('what.ever', sys.argv[2])
config_Pd113 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_Pd113)

# import experiment-parameters-file as a module to get wavelength
import importlib
spec = importlib.util.spec_from_file_location('what.ever', sys.argv[3])
exper_param = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exper_param)

source_directory = sys.argv[1]
output_file = sys.argv[4]

collector = []

for filename in os.listdir(source_directory):
    basename = os.path.basename(filename)
    root = basename.split('.')[0]
    pattern_no = int(root)
    pattern = np.loadtxt(os.path.join(source_directory, filename))
    peak_pos = peak_position(pattern, config_Pd113.twotheta_interval_Pd113)
    lcc = latt_ct_cubic(exper_param.wavelength, peak_pos, config_Pd113.plane)
    collector.append([pattern_no, peak_pos, lcc])


collector.sort(key=lambda data_point: data_point[0]) #sort by pattern_no

header = \
"""# Use with caution!  These values are determined with a simple algorithm
# (2theta value of data point with highest intensity in a given interval).
# Many of the values are simply incorrect!
# The algorithm may be upgraded in the future."""

with open(output_file, "w") as output:
    output.write(header + '\n')
    for [pattern_no, peak_pos, lcc] in collector:
        output.write("{} {} {}\n".format(str(pattern_no), str(peak_pos),
                                         str(lcc)))

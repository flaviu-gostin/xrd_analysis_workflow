"""Determine peak positions for all patterns in given directory.

Usage:
python determine_peak_position.py source_dir config_file output_file

A peak position value will be determined for each file in 'source_dir'.  Each
peak position value will be prefixed with the source file basename and written
to 'output_file'.  The source file basename must consist of integers only,
e.g. '0.dat' or '23.dat'.

"""
import numpy as np
import os
from collections import OrderedDict
import sys
#workaround to be able to append "functions" irrespective of cwd
script_abspath = os.path.abspath(sys.argv[0])
common_path = os.path.dirname(os.path.dirname(script_abspath))
sys.path.append(os.path.join(common_path, 'functions'))
from peak_calc import peak_position

import importlib
spec = importlib.util.spec_from_file_location('what.ever', sys.argv[2])
config_Pd113 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_Pd113)


source_directory = sys.argv[1]
output_file = sys.argv[3]

d = {}

for filename in os.listdir(source_directory):
    basename = os.path.basename(filename)
    root = basename.split('.')[0]
    root = int(root)
    pattern = np.loadtxt(os.path.join(source_directory, filename))
    pp = peak_position(pattern, config_Pd113.twotheta_interval_Pd113)
    d[root] = pp #Should be e.g. {23:32.7893, 11:32.7392, ...}


d_ordered = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

header = \
'# Use with caution.  These values are determined with a simple algorithm'

with open(output_file, "w") as output:
    output.write(header + '\n')
    for k, v in d_ordered.items():
        output.write("{} {}\n".format(str(k), str(v)))

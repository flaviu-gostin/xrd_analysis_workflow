"""
Create table containing the lattice constant of Pd calculated from the 
position of the 113 peak.

"""
import numpy as np
import os
import sys
sys.path.append("../functions/")
from peak_calc import latt_ct_avg 

wl = 0.6907e-10    # Wavelength in meter
roi_Pd113 = (33.5, 34.6)    # (start, end) values of 2theta interval of Pd113
location_stacks = "../../results/intermediate/integrated_1D/"

"""scans_patterns is a list giving the directories in location_stacks
where 1D patterns are, and patterns used for calculating the average
lattice spacing of Pd as a tuple (first pattern, last pattern + 1, step)"""
scans_patterns = [["PS_1p3V_b", (0, 82)],
                  # ["PSA_1p3V_c", (0, 44)],
                  # ["PSP_1p3V_b", (0, 63)],
                  # ["PSAP_1p3V_a", (10, 31)],
                  # ["PS_0p7V_b", (0, 69)],
                  # ["PS_0p5V_b", (0, 119)],
                  # ["PS_0p0V_a", (143, 148)],
                  # ["PS_0p0V_a", (69, 74)],
                  ["PS_0p0V_a", (0, 5)]]

results_file = "../../results/final/table_Pd_summary.txt"


with open(results_file, "w") as rf:
    rf.write("# This is a summary table of lattice spacing values determined from the Pd113 peak \n")
    for [scan, patterns] in scans_patterns:
        dir_1D = location_stacks + scan + "/"
        lca = latt_ct_avg(dir_1D, patterns, wl)
        #e is the electrolyte
        e = scan.split('_')[0]
        #p is the potential
        p = scan.split('_')[1]
        rf.write(e + "     " + p + "    " +
                 str(np.around(lca, decimals=4)) + "\n")

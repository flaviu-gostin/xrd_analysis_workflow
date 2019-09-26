"""
Create table containing the lattice constant of Pd calculated from the 
position of the 113 peak.

"""
import numpy as np
import os
import sys
sys.path.append("../functions/")
from peak_calc import peak_maxima, latt_ct

wl = 0.6907e-10    # Wavelength in meter
cryst_syst_Pd = "cubic"    # Crystal system of Pd
# (start, end) values of 2theta interval of Pd113
tth_int_Pd113 = (33.5, 34.6)
planes_Pd113 = (1, 1, 3)
location_stacks = "../../results/intermediate/integrated_1D/"

"""scans_patterns is a list giving the directories in location_stacks
where 1D patterns are, and patterns used for calculating the average
lattice spacing of Pd as a tuple (first pattern, last pattern + 1, step)"""
scans_patterns = [["PS_1p3V_b", (0, 82)],
                  ["PSA_1p3V_c", (0, 44)],
                  ["PSP_1p3V_b", (0, 63)],
                  ["PSAP_1p3V_a", (10, 31)],
                  ["PS_0p7V_b", (0, 69)],
                  ["PS_0p5V_b", (0, 119)],
                  ["PS_0p0V_a", (143, 148)],
                  ["PS_0p0V_a", (69, 74)],
                  ["PS_0p0V_a", (0, 5)]]
results_file = "../../results/final/table_Pd_summary.txt"

table_header = \
"""
Table.  Lattice constant and crystallite size of Pd particles
generated inside artificial pits on Ti40Zr10Cu34Pd14Sn2 metallic glass
ribbons.
---------------------------------------------
{:<15}{:<12}{}
---------------------------------------------
""".format("Electrolyte", "Potential", "Lattice constant")

with open(results_file, "w") as rf:
    rf.write(table_header)
    for [scan, patterns] in scans_patterns:
        dir_1D = location_stacks + scan + "/"
        # pm contains 2theta values of Pd113 peak max for each pattern
        pm = peak_maxima(dir_1D, patterns, tth_int_Pd113)
        # lc calculates lattice constant values from 2theta values in pm
        lc = [latt_ct(wl, i, cryst_syst_Pd, planes_Pd113) for i in pm]
        lca = np.mean(lc, dtype=np.float64)    # Average over lc
        lcsd = np.std(lc, dtype=np.float64)    # St dev over lc
        lcsd_1signif = '{:.1g}'.format(lcsd)    # Round to 1 signif digit
        # Get the no of decimals of lcsd_signif
        decimals_no = len(str(lcsd_1signif).split('.')[1])
        # ... and apply it to lca
        lca_signif = '{:.{dec_no}f}'.format(lca, dec_no=decimals_no)
        # lcsd_1 is a single digit: the first significant figure
        lcsd_1 = str(lcsd_1signif)[-1]
        e = scan.split('_')[0]    # the electrolyte
        p = scan.split('_')[1]    # the potential
        p_better = p.replace("p", ".")
        rf.write("{:<15}{:<12}{}({})\n".format(e, p_better, lca_signif,
                                               lcsd_1))
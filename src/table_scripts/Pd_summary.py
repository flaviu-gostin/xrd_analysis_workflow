"""
Create table containing the lattice constant of Pd calculated from the
position of the 113 peak.

Usage: python3 Pd_summary.py source-dir table-file

source-dir : directory where files with peak position data can be found
table-file : file to write the table to

"""
import numpy as np
import os
import sys


source_dir = sys.argv[1]
table_file = sys.argv[2]

# scans_patterns is a list of scans and the patterns used for calculating the
# average lattice constant of Pd for each scan, as a tuple (first_pattern,
# last_pattern)
scans_patterns = [["PS_1p3V_b", (0, 81)],
                  ["test-PS_1p3V_b", (0, 1)],
                  ["PSA_1p3V_c", (0, 42)],
                  ["PSP_1p3V_b", (0, 62)],
                  ["test-PSP_1p3V_b", (0, 1)],
                  ["PSAP_1p3V_a", (10, 30)],
                  ["PS_0p7V_b", (0, 69)],
                  ["PS_0p5V_b", (0, 100)],
                  ["PS_0p0V_a", (143, 147)],
                  ["PS_0p0V_a", (69, 73)],
                  ["PS_0p0V_a", (0, 4)]]

# desired width for each column in table (in no of characters)
l = [18, 12, 18, 3]
hline = '-' * sum(l) #horizontal lines in the table

table_header = """\
Table.  Lattice constant and crystallite size of Pd particles generated inside
artificial pits on Ti40Zr10Cu34Pd14Sn2 metallic glass ribbons.
{4}
{0:{5}}{1:{6}}{2:{7}}{3:{8}}
{4}
""".format("Electrolyte", "Potential", "Lattice ct", "n", hline, l[0], l[1],
           l[2], l[3])

def row_formater(el, pot, latt_ct, n, len_cols):
    """Arrange arguments to print nicely in the table

    Parameters
    ----------
    col_el : str
        String for the 'Electrolyte' column
    col_X : str
        String for the 'X' column
    len_cols : list
        List with widths for each column

    Returns
    -------
    row : str
        String representing the row

    """
    l = len_cols
    return "{0:{4}}{1:{5}}{2:{6}}{3:{7}}\n".format(el, pot, latt_ct, n, l[0],
                                                   l[1], l[2], l[3])


with open(table_file, "w") as rf:
    rf.write(table_header)
    for [scan, (st, end)] in scans_patterns:
        filename = os.path.join(source_dir, scan + '_Pd113.dat')
        try:
            data_all = np.loadtxt(filename, usecols=2)
        except OSError:
            continue
        data = data_all[st:end + 1]
        n = end - st + 1

        # Calculate and report the average lattice constant as e.g. 3.895(2) A
        # Average lattice constant (float64 for better precision)
        latt_ct_avg = np.mean(data, dtype=np.float64)
        # ... and the standard deviation
        latt_ct_stdev = np.std(data, dtype=np.float64)
        # Round it to 1 signif digit
        latt_ct_stdev_rounded_to_1_signifdig = '{:.1g}'.format(latt_ct_stdev)
        # Get the no of decimals
        decimals_no = len(str(
            latt_ct_stdev_rounded_to_1_signifdig).split('.')[1])
        # ... and apply it to the average
        latt_ct_avg_signif = '{:.{dec_no}f}'.format(latt_ct_avg,
                                                    dec_no=decimals_no)
        # get just the first significant figure
        latt_ct_stdev_digit = str(latt_ct_stdev_rounded_to_1_signifdig)[-1]
        latt_ct_final = "{}({})".format(latt_ct_avg_signif, latt_ct_stdev_digit)

        e = scan.split('_')[0]    # the electrolyte
        p = scan.split('_')[1]    # the potential
        p_better = p.replace("p", ".")
        p_better = p_better.replace("V", " V")

        row = row_formater(e, p_better, latt_ct_final, n, l)
        rf.write(row)

    rf.write(row_formater("Standard pure Pd", "", "3.89", "", l))
    rf.write(row_formater("alpha-PdHx max", "", "3.91", "", l))
    rf.write(row_formater("beta-PdHx min", "", "3.97", "", l))

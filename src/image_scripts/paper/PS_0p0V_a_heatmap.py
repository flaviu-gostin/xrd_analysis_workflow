"""Create powder diffraction heatmap figure for PS at 0 V

Run with: python3 PS_0p0V_a_heatmap.py

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import os
import sys

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_0p0V_a"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_0p0V_a_heatmap.svg"

references = ['Pd', 'Cu', 'CuCl', 'Cu20']
position_subplot_measured=3


measured_patterns_fns_unsorted = os.listdir(measured_patterns_dir)
#sort in order: 0.dat, 1.dat, ..., 10.dat, ...
measured_patterns_fns = sorted(measured_patterns_fns_unsorted, key=lambda fn:
                               int(fn.split(sep='.')[0]))
start, stop, step = 0, len(measured_patterns_fns), 1
patterns_to_plot = list(range(start, stop, step))

l = []
for pattern_no in patterns_to_plot:
    d = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern_no) +
                                '.dat'))
    y = d[:,1]
    l.append(y) # l is a list of numpy arrays (that should be ok, right?)

data = np.vstack(tuple(l))


fig, ax = plt.subplots()
fig.set_size_inches(3.5, 5)
fig.set_dpi(1000)
fig.subplots_adjust(left=0.1, right=0.84, top=0.98, bottom=0.08)
im = ax.imshow(data, cmap='gnuplot', aspect=50, interpolation='none', vmin=3000,
               vmax=20000)

cbar = plt.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Intensity, a.u.')

#Label ticks on X axis with 2theta values
x, __ = np.loadtxt(os.path.join(measured_patterns_dir, '0.dat'), unpack=True)
xticks = np.arange(0, 4001, 1000)
ax.set_xticks(xticks)
r = np.around(x[xticks]) #2theta values at given indices (rounded to 0 decimals)
twotheta_labels = r.astype(int) #do not show the decimal point
ax.set_xticklabels(twotheta_labels)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set(xlabel=r'$2\theta$, degree')


fig.savefig(figure_fn)

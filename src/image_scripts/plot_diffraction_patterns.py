"""Plot stack of measured and calculated diffraction patterns (X=2theta)

Create a figure containing multiple subfigures.  One subfigure contains a
sequence of measured diffraction patterns.  Each of the other subfigures is a
stick plot of calculated Bragg reflections of a reference phase.

Run with: python plot_diffraction_patterns.py

"""
import matplotlib.pyplot as plt
import numpy as np
import os

measured_dir = "../../results/intermediate/integrated_1D/PS_1p3V_b"
figure_fn = "diffraction_patterns.svg"

width_single_column = 3.5 #inch
width_onehalf_column = 5 #inch
width_two_column = 7.2 #inch

fig = plt.figure()
#fig.set_dpi(500)
fig.set_figwidth(width_single_column)

ax_measured = fig.add_subplot(1, 1, 1)
offset = 5000
fns = os.listdir(measured_dir)
sorted_fns = sorted(fns, key=lambda fn: int(fn.split(sep='.')[0]))
for idx, fn in enumerate(sorted_fns):
    data = np.loadtxt(os.path.join(measured_dir, fn))
    ax_measured.plot(data[:,0], data[:,1] - offset * idx, linewidth=0.5)

fig.savefig(figure_fn)

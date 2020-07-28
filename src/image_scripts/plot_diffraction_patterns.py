"""Plot stack of measured and calculated diffraction patterns (x=2theta)

Create a figure containing multiple subfigures.  One subfigure contains a
sequence of measured diffraction patterns.  Each of the other subfigures is a
stick plot of calculated Bragg reflections of a reference phase.

Run with: python plot_diffraction_patterns.py

"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

measured_patterns_dir = "../../results/intermediate/integrated_1D/PS_1p3V_b"
figure_fn = "diffraction_patterns.svg"

label_every_nth_pattern = 5

# TODO: use this dict to draw vertical lines on the right side of the figure
#indicating patterns containing peaks of given phase(s)
# TODO: need to get more accurate values for this dict
layers = {'Pd': (0, 84), #not sure about the end
          'PdCl2': (15, 64), #~OK
          'X1+X2': (54, 70), #~OK
          'X3+X4': (67,81), #OK
          'CuCl': (72, 88), #~OK
          'MG': (85, 100)} #not sure about start

standard_fig_widths_inch = {'single_column': 3.5,
                            'onehalf_column': 5,
                            'two_column': 7.2}
figwidth = standard_fig_widths_inch['single_column']
figheight = figwidth * 1.5
global_linewidth = 0.4
mpl.rcParams['axes.linewidth'] = global_linewidth
#plt.rcParams.update({'figure.autolayout': True})


fig = plt.figure()
#fig.set_dpi(500)    useless for vector graphics?
fig.set_figwidth(figwidth)
fig.set_figheight(figheight)

#plot the measured patterns
ax_measured = fig.add_subplot(1, 1, 1)
ax_measured.tick_params(axis='y', which='both', left=False, labelleft=False)
ax_measured.set_ylabel("Relative intensity")
ax_measured.set(xlim=[2, 41], xlabel="2theta, degree")
offset_patterns = 2000
fns = os.listdir(measured_patterns_dir) #this is not sorted
#sort in order: 0.dat, 1.dat, ..., 10.dat, ...
sorted_fns = sorted(fns, key=lambda fn: int(fn.split(sep='.')[0]))

#plot data and label patterns with numbers
for idx, fn in enumerate(sorted_fns):
    data = np.loadtxt(os.path.join(measured_patterns_dir, fn))
    x_vals, y_vals = data[:,0], data[:,1] - offset_patterns * idx
    line, = ax_measured.plot(x_vals, y_vals)
    line.set_linewidth(global_linewidth)
    if idx % label_every_nth_pattern == 0:
        label_text = fn.split(sep='.')[0]
        idx_rightmost_point = np.searchsorted(x_vals, ax_measured.get_xlim()[1],
                                              side='right') - 1
        x_ref, y_ref = x_vals[idx_rightmost_point], y_vals[idx_rightmost_point]
        label = ax_measured.annotate(label_text, (x_ref, y_ref),
                                      textcoords="offset points", xytext=(2,0),
                                      va='center')
        label.set_fontsize('xx-small')

#label layers, e.g. "Pd", "PdCl2"
for k, v in layers.items():
    label_text = k
    for pattern_no in v:
        label_text = k if pattern_no == v[0] else "x" + k
        data = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern_no) +
                                       '.dat'))
        x_vals, y_vals = data[:,0], data[:,1] - offset_patterns * pattern_no
        idx_rightmost_point = np.searchsorted(x_vals, ax_measured.get_xlim()[1],
                                              side='right') - 1
        x_ref, y_ref = x_vals[idx_rightmost_point], y_vals[idx_rightmost_point]
        box = ax_measured.annotate(label_text, (x_ref, y_ref),
                                   textcoords="offset points",
                                   xytext = (2 + 12 , 0), va='center')

# add stick plot(s) for reference phases

fig.savefig(figure_fn)

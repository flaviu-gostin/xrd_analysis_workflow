"""Plot stack of measured and calculated diffraction patterns (x=2theta)

Create a figure containing multiple subfigures.  One subfigure contains a
sequence of measured diffraction patterns.  Each of the other subfigures is a
stick plot of calculated Bragg reflections of a reference phase.

Run with: python plot_diffraction_patterns.py [patterns]

patterns : two integers separated by one colon, e.g. '21:67' plots all patterns
from 21 to 66 (stop position 67 is not plotted).  If omitted, all available
patterns are plotted.

"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

measured_patterns_dir = "../../results/intermediate/integrated_1D/PS_1p3V_b"
figure_fn = "diffraction_patterns.svg"

measured_patterns_fns_unsorted = os.listdir(measured_patterns_dir)
#sort in order: 0.dat, 1.dat, ..., 10.dat, ...
measured_patterns_fns = sorted(measured_patterns_fns_unsorted,
                               key=lambda fn: int(fn.split(sep='.')[0]))

try:
    positions = sys.argv[1].split(sep=':')
    start, stop = [int(position) for position in positions]
except IndexError:
    start, stop = 0, len(measured_patterns_fns)

patterns_to_plot = list(range(start, stop))

label_every_nth_pattern = 5

# TODO: use this dict to draw vertical lines on the right side of the figure
#indicating patterns containing peaks of given phase(s)
# TODO: need to get more accurate values for this dict
layers = {'Pd': (0, 84), #not sure about the end
          'PdCl2': (4, 65), #OK
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
fig.subplots_adjust(left=0.06, right=0.755, bottom=0.085, top=0.995,
                    wspace=0.2, hspace=0.2)

#plot the measured patterns
ax_measured = fig.add_subplot(1, 1, 1)
ax_measured.tick_params(axis='y', which='both', left=False, labelleft=False)
ax_measured.set_ylabel("Relative intensity")
ax_measured.set(xlim=[2, 41], xlabel="2theta, degree")
offset_patterns = 2000


#plot data and label patterns with numbers
for pattern_no in patterns_to_plot:
    data = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern_no) +
                                   '.dat'))
    x_vals, y_vals = data[:,0], data[:,1] - offset_patterns * pattern_no
    line, = ax_measured.plot(x_vals, y_vals)
    line.set_linewidth(global_linewidth)
    if pattern_no % label_every_nth_pattern == 0:
        label_text = str(pattern_no)
        idx_rightmost_point = np.searchsorted(x_vals, ax_measured.get_xlim()[1],
                                              side='right') - 1
        x_ref, y_ref = x_vals[idx_rightmost_point], y_vals[idx_rightmost_point]
        label = ax_measured.annotate(label_text, (x_ref, y_ref),
                                      textcoords="offset points", xytext=(2,0),
                                      va='center')
        label.set_fontsize('xx-small')

#label layers, e.g. "Pd", "PdCl2"
for idx, (k, v) in enumerate(layers.items()):
    #add upper and (empty) lower annotation boxes
    label_text = k
    data_top = np.loadtxt(os.path.join(measured_patterns_dir, str(v[0]) +
                                       '.dat'))
    data_bottom = np.loadtxt(os.path.join(measured_patterns_dir, str(v[1]) +
                                          '.dat'))
    x_vals_top, y_vals_top = data_top[:,0], data_top[:,1] - offset_patterns *\
                             v[0]
    x_vals_bottom, y_vals_bottom = data_bottom[:,0], data_bottom[:,1] -\
                                   offset_patterns * v[1]
    idx_rightmost_point_top = np.searchsorted(x_vals_top,
                                              ax_measured.get_xlim()[1],
                                              side='right') - 1
    idx_rightmost_point_bottom = np.searchsorted(x_vals_bottom,
                                              ax_measured.get_xlim()[1],
                                              side='right') - 1
    x_ref_top, y_ref_top = x_vals_top[idx_rightmost_point_top],\
    y_vals_top[idx_rightmost_point_top]
    x_ref_bottom, y_ref_bottom = x_vals_bottom[idx_rightmost_point_bottom],\
    y_vals_bottom[idx_rightmost_point_bottom]
    ann_top = ax_measured.annotate(label_text, (x_ref_top, y_ref_top),
                                   textcoords="offset points",
                                   xytext = (2 + 12 + idx * 4, 0), va='center')
    ann_bottom = ax_measured.annotate('', (x_ref_bottom, y_ref_bottom),
                                      textcoords="offset points",
                                      xytext = (2 + 12 + idx * 4, 0),
                                      va='center')

    #add line between upper and lower annotation boxes
    ax_measured.annotate('', xy=(0, 0.7), xycoords=ann_top,
                         xytext=(0, 0.3), textcoords=ann_bottom,
                         arrowprops={'arrowstyle': '-',
                                     'linewidth': global_linewidth})


# add stick plot(s) for reference phases

fig.savefig(figure_fn)

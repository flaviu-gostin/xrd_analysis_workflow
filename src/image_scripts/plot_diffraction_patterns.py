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
reference_peaks_dir = "../../results/intermediate/peaks_references"
references_fnames = {'Pd': 'Pd.dat',
                     'PdCl2': 'PdCl2.dat',
                     'CuCl': 'CuCl.dat'}
references_colors = {'Pd': 'blue',
                     'PdCl2': 'red',
                     'CuCl': 'green'}
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
position_measured = 3 #1 is first from the top
height_ratio_measured_to_reference = 5

twotheta_range = [2, 41]
offset_patterns = 2000
label_every_nth_pattern = 5

layers = {'Pd': {'patterns': (0, 83), 'label': 'Pd', 'color': 'blue'},
          'PdCl2': {'patterns': (4, 65), 'label': r'PdCl$_2$', 'color': 'red'},
          'X1+X2': {'patterns': (52, 70), 'label': 'X1+X2', 'color': 'black'},
          'CuCl': {'patterns': (66, 89), 'label': 'CuCl', 'color': 'green'},
          'X3+X4': {'patterns': (67, 81), 'label': 'X3+X4', 'color': 'black'},
          'MG': {'patterns': (77, 100), 'label': 'MG', 'color': 'magenta'}}

# Label positions
offset_numbering_labels = 2 #figure points
offset_layer_lines = 14
offset_line_to_line = 9

standard_fig_widths_inch = {'single_column': 3.5,
                            'onehalf_column': 5,
                            'two_column': 7.2}
figwidth = standard_fig_widths_inch['single_column']
figheight = figwidth * 1.5
global_linewidth = 0.4
mpl.rcParams['axes.linewidth'] = global_linewidth
#plt.rcParams.update({'figure.autolayout': True})


def xydata(pattern):
    """ Prepare data for plotting for a given pattern

    pattern : integer
    out : two numpy 1D arrays

    """
    d = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern) + '.dat'))
    x, y = d[:,0], d[:,1] - offset_patterns * pattern
    return x, y


def xy_rightmost_point(x, y, ax):
    """ Determine the coordinates of the rightmost visible point in a subplot

    x, y : two numpy 1D arrays
    ax: subplot(axes) in which x, y is plotted
    out : two floats

    """
    idx = np.searchsorted(x, ax.get_xlim()[1], side='right') - 1
    return x[idx], y[idx]


# Set up the figure
no_subplots = len(references_fnames) + 1
height_ratios = [1 for i in references_fnames]
height_ratios.insert(position_measured - 1, height_ratio_measured_to_reference)
# e.g. [1, 1, 5 ,1] means 3rd cell is 5x higher than 1st, 2nd and 4th
fig, axs = plt.subplots(nrows=no_subplots, sharex=True,
                       gridspec_kw=dict(height_ratios=height_ratios))
ax_measured = axs[position_measured -1]
axs_refs = axs[axs != ax_measured] #numpy boolean indexing

axs[0].set(xlim=twotheta_range) #set early to prevent label misplacement

#fig.set_dpi(500)    useless for vector graphics?
fig.set_figwidth(figwidth)
fig.set_figheight(figheight)
fig.subplots_adjust(left=0.06, right=0.75, bottom=0.085, top=0.995,
                    wspace=0.2, hspace=0.05)


def plot_powder_diffraction(measured_patterns_dir=None, patterns=None,
                            position_measured=None, ref_fnames=None):
    """ Create and plot powder diffraction figure.

    Parameters
    ----------
    measured_patterns_dir : str
        Directory containing data for measured patterns to plot.  The base of
        the file names must be integers, e.g. '0.dat', '23.txt'
    patterns : tuple
        tuple with two integers, e.g. '(21, 67)' plots all patterns from 21 to
        66.  If omitted, all available patterns are plotted.
    position_measured : integer
        Position in figure of measured patterns subplot.  Counting starts at 1
        from the top.
    ref_fnames : list
        List of file names as strings.  Each file contains diffraction peaks
        for a reference phase.  First column is the 2theta value, ...
    ... : ...
        ...

    Returns
    -------
    out : matplotlib figure


    """
    pass


# Set up subplot for measured patterns
#ax_measured.set_box_aspect(3/1) #Don't use this.  Use gridspec_kw in fig
ax_measured.tick_params(axis='y', which='both', left=False, labelleft=False)
ax_measured.set_ylabel("Relative intensity")


# Plot measured patterns and label them with numbers
for pattern_no in patterns_to_plot:
    x_vals, y_vals = xydata(pattern_no)
    line, = ax_measured.plot(x_vals, y_vals)
    line.set_linewidth(global_linewidth)
    if pattern_no % label_every_nth_pattern == 0:
        label_text = str(pattern_no)
        #don't change xlim from this point on (it might affect labels positions)
        __, y_ann = xy_rightmost_point(x_vals, y_vals, ax_measured)
        label = ax_measured.annotate(label_text, xy=(1, y_ann),
                                     xycoords=('axes fraction', 'data'),
                                     xytext=(offset_numbering_labels, 0),
                                     textcoords="offset points", va='center')
        label.set_fontsize('xx-small')


# Label layers, e.g. "Pd", "PdCl2", height shown by vertical lines
for idx, (layer_name, layer_attributes) in enumerate(layers.items()):
    layer_first_pattern, layer_last_pattern = layer_attributes['patterns']
    top_pattern = max(layer_first_pattern, patterns_to_plot[0])
    bottom_pattern = min(layer_last_pattern, patterns_to_plot[-1])
    xtop, ytop = xydata(top_pattern)
    xbottom, ybottom = xydata(bottom_pattern)
    __, y_ann_top = xy_rightmost_point(xtop, ytop, ax_measured)
    __, y_ann_bottom = xy_rightmost_point(xbottom, ybottom, ax_measured)

    #Don't let lines run above top of subplot
    if y_ann_top > ax_measured.get_ylim()[1]:
        y_ann_top = ax_measured.get_ylim()[1]

    #Don't let lines run below bottom of subplot
    if y_ann_bottom < ax_measured.get_ylim()[0]:
        y_ann_bottom = ax_measured.get_ylim()[0]

    #Create layer labels only if top pattern is above bottom of subplot
    if y_ann_top > ax_measured.get_ylim()[0] and \
       y_ann_bottom < ax_measured.get_ylim()[1]:
        color = layer_attributes['color']
        xtext = offset_layer_lines + idx * offset_line_to_line
        yadjustment = 2 #points
        label_text = layer_attributes['label']
        ann_top = ax_measured.annotate(label_text, xy=(1, y_ann_top),
                                       xycoords=('axes fraction', 'data'),
                                       xytext=(xtext, yadjustment),
                                       textcoords='offset points', va='bottom',
                                       ha='center', rotation=90, color=color)
        ann_bottom = ax_measured.annotate('', xy=(1, y_ann_bottom),
                                          xycoords=('axes fraction', 'data'),
                                          xytext=(xtext, -yadjustment),
                                          textcoords="offset points",
                                          va='center')
        # add line between upper and lower annotation boxes
        ax_measured.annotate('', xy=(0.5, 0), xycoords=ann_top,
                             xytext=(0, 0.3), textcoords=ann_bottom,
                             arrowprops={'arrowstyle': '-', 'color': color,
                                         'linewidth': global_linewidth})


# Add stick plot(s) for reference phases
#ax_ref1.set_box_aspect(1/4) #Don't use this.  Use gridspec_kw in fig


def xydata_reference(filename):
    """ Extract xy data from a file containing Bragg peaks for a reference """
    data = np.loadtxt(os.path.join(reference_peaks_dir, filename))
    twotheta, intensity = data[:,0], data[:,1]
    return twotheta, intensity


def stick_plotter(ax, reference_name, twotheta, intensity, color):
    """ Make a stick plot in a given axes for a given reference """
    stem_container = ax.stem(twotheta, intensity)
    stem_container.baseline.set_visible(False)
    stem_container.markerline.set_visible(False)
    stem_container.stemlines.set_color(color)
    ax.annotate(reference_name, xy=(1, 1), xycoords='axes fraction',
                xytext=(10, 0), textcoords='offset points', va='top',
                color=color)


# Plot stick plots for references and label them
for ax, (ref, fname) in zip(axs_refs, references_fnames.items()):
    twotheta, intensity = xydata_reference(fname)
    stick_plotter(ax, ref, twotheta, intensity, references_colors[ref])
    ax.set(ylim=[0, 110])
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)


# Axis
# Set up label for X axis for bottom subplot
axs[-1].set(xlabel=r'$2\theta$, degree') #ticks labels by default
# No label and ticks labels for X axis for the other subplots
for ax in axs[:-1]:
    plt.setp(ax.get_xticklabels(), visible=False)


fig.savefig(figure_fn)
#plt.grid()
#plt.show()

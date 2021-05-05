"""This module provides a function to create a powder diffraction figure.

Create a figure containing multiple subfigures aligned vertically.  One
subfigure contains a sequence of measured diffraction patterns.  Each of the
other subfigures is a stick plot of calculated Bragg reflections of a reference
phase.

"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os
import sys


def powder_diffr_fig(measured_patterns_dir=None,
                     patterns=None,
                     position_subplot_measured=1,
                     reference_peaks_dir=None,
                     references=None,
                     height_ratio_measured_to_reference=7,
                     twotheta_range=[2, 41],
                     offset_patterns=2000,
                     label_every_nth_pattern=5,
                     offset_numbering_labels=2,
                     layers=None,
                     offset_layer_lines = 14,
                     offset_line_to_line = 9,
                     figwidth='single_column',
                     linewidth=0.6):
    """Return powder diffraction figure and its axes.

    Create a matplotlib figure containing several subfigures aligned vertically.
    One subfigure plots a sequence of measured powder diffraction patterns.  The
    other subfigures are stick plots for selected reference patterns.  The
    default figure settings are for single column width in a typical journal.

    Parameters
    ----------
    measured_patterns_dir : str
        Directory containing data for measured patterns to plot.  The base of
        the file names must be integers, e.g. '0.dat', '23.txt'
    patterns : tuple
        Tuple with three integers, e.g. '(21, 67, 2)' plots every second pattern
        from 21 to 66.  If omitted, all available patterns are plotted.
    position_subplot_measured : integer
        Position in figure of the subfigure plotting the measured patterns.
        Counting starts at 1 from the top.
    reference_peaks_dir : str
        Directory containing files with peak data for reference phases.
    references : list
        List of references as strings, e.g. 'Pd', 'PdCl2'
    height_ratio_measured_to_reference : integer
        Height ratio of subplots for measured patterns and reference patterns.
    twotheta_range : list with two floats
        List with two values: beginning and end of x axis.
    offset_patterns : float
        Offset each pattern by given offset from previous one.
    label_every_nth_pattern : int
        Label only patterns of which sequence number are multiples of n.
    offset_numbering_labels : integer
        Number of figure points by which pattern number labels are offset from
        the right edge of the subfigure.
    layers : dict
        Dictionary.  Each item corresponds to a layer.  The key is a string
        giving the name of the reference phase in that layer.  The value is a
        tuple of two integers representing the first and the last pattern in
        that layer.
    offset_layer_lines : int
        Number of figure points by which the first vertical line is offset from
        the right edge of the subfigure.
    offset_line_to_line : int
        Offset of each line from the previous in figure points.
    figwidth : float or string
        Figure width in inch.  Accepts certain strings.  See below.
    linewidth : float
        Global linewidth for this figure.

    Returns
    -------
    out : matplotlib figure and its axes

    """
    refs_labels_style = {'Pd': {'label': 'Pd', 'color': 'blue'},
                         'PdCl2': {'label': r'PdCl$_2$', 'color': 'red'},
                         'X1+X2': {'label': 'X1+X2', 'color': 'black'},
                         'CuCl': {'label': 'CuCl', 'color': 'green'},
                         'X3+X4': {'label': 'X3+X4', 'color': 'black'},
                         'ZrOCl2_8H2O': {'label': r'ZrOCl$_2$' + '\n' +
                                         r'$\cdot$8H$_2$O', 'color': 'red'},
                         'Cu': {'label': 'Cu', 'color': 'red'},
                         'Cu2O': {'label': r'Cu$_2$O', 'color': 'black'},
                         'Pd3.97': {'label': r'Pd ($\beta$ PdH$_x$)' + '\n' +
                                    r'$a = 3.97 \AA$', 'color': 'red'},
                         'Pd3.91': {'label': r'Pd ($\alpha$ PdH$_x$)' + '\n' +
                                    r'$a = 3.91 \AA$', 'color': 'black'},
                         'MG': {'label': 'MG', 'color': 'magenta'},
                         'Corrosion\nproducts': {'label': 'Corrosion\nproducts',
                                                 'color': 'black'},
                         'Metallic\nglass': {'label': 'Metallic\nglass',
                                             'color': 'magenta'}}

    references_fnames = [ref + '.dat' for ref in references]

    measured_patterns_fns_unsorted = os.listdir(measured_patterns_dir)
    #sort in order: 0.dat, 1.dat, ..., 10.dat, ...
    measured_patterns_fns = sorted(measured_patterns_fns_unsorted,
                               key=lambda fn: int(fn.split(sep='.')[0]))


    # What patterns to plot
    if not patterns:
        start, stop, step = 0, len(measured_patterns_fns), 1
    else:
        start, stop, step = patterns

    patterns_to_plot = list(range(start, stop, step))


    # Figure dimensions
    standard_figwidths_inch = {'single_column': 3.5,
                                'onehalf_column': 5,
                                'two_column': 7.2}
    if isinstance(figwidth, str):
        figwidth = standard_figwidths_inch[figwidth]

    figheight = figwidth * 1.5
    mpl.rcParams['axes.linewidth'] = linewidth


    def xydata(pattern):
        """ Prepare data for plotting a given pattern

        pattern : int
        out : two numpy 1D arrays

        """
        d = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern) +
                                    '.dat'))
        x, y = d[:,0], d[:,1] - offset_patterns * pattern
        return x, y


    def xy_rightmost_point(x, y, ax):
        """Determine the coordinates of the rightmost visible point in a subplot

        x, y : two numpy 1D arrays
        ax: subplot(axes) in which x, y is plotted
        out : two floats

        """
        idx = np.searchsorted(x, ax.get_xlim()[1], side='right') - 1
        return x[idx], y[idx]


    # Set up the figure
    no_subplots = len(references) + 1
    height_ratios = [1 for i in references]
    height_ratios.insert(position_subplot_measured - 1,
                         height_ratio_measured_to_reference)
    # e.g. [1, 1, 5 ,1] means 3rd cell is 5x higher than 1st, 2nd and 4th
    fig, axs = plt.subplots(nrows=no_subplots, sharex=True,
                           gridspec_kw=dict(height_ratios=height_ratios))
    ax_measured = axs[position_subplot_measured -1]
    axs_refs = axs[axs != ax_measured] #numpy boolean indexing

    axs[0].set(xlim=twotheta_range) #set early to prevent label misplacement

    #fig.set_dpi(500)    useless for vector graphics?
    fig.set_figwidth(figwidth)
    fig.set_figheight(figheight)
    fig.subplots_adjust(left=0.06, right=0.75, bottom=0.085, top=0.995,
                        wspace=0.2, hspace=0.05)


    # Set up subplot for measured patterns
    #ax_measured.set_box_aspect(3/1) #Don't use this.  Use gridspec_kw in fig
    ax_measured.tick_params(axis='y', which='both', left=False, labelleft=False)
    ax_measured.set_ylabel("Relative intensity")


    # Plot measured patterns and label them with numbers
    for pattern_no in patterns_to_plot:
        x_vals, y_vals = xydata(pattern_no)
        line, = ax_measured.plot(x_vals, y_vals)
        line.set_linewidth(linewidth)
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
    if layers:
        for idx, layer_name in enumerate(layers.keys()):
            layer_first_pattern, layer_last_pattern = layers[layer_name]
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
                style = refs_labels_style[layer_name]
                color = style['color']
                xtext = offset_layer_lines + idx * offset_line_to_line
                yadjustment = 2 #points
                label_text = style['label']
                ann_top = ax_measured.annotate(label_text, xy=(1, y_ann_top),
                                               xycoords=('axes fraction',
                                                         'data'),
                                               xytext=(xtext, yadjustment),
                                               textcoords='offset points',
                                               va='bottom', ha='center',
                                               rotation=90, color=color)
                ann_bottom = ax_measured.annotate('', xy=(1, y_ann_bottom),
                                                  xycoords=('axes fraction',
                                                            'data'),
                                                  xytext=(xtext, -yadjustment),
                                                  textcoords="offset points",
                                                  va='center')
                # add line between upper and lower annotation boxes
                ax_measured.annotate('', xy=(0.5, 0), xycoords=ann_top,
                                     xytext=(0, 0.3), textcoords=ann_bottom,
                                     arrowprops={'arrowstyle': '-',
                                                 'color': color,
                                                 'linewidth': linewidth})


    def xydata_reference(filename):
        """Extract xy data from a file containing Bragg peaks for a reference"""
        twotheta, intensity = \
        np.loadtxt(os.path.join(reference_peaks_dir, filename), usecols=(0,1),
                   unpack=True)
        return twotheta, intensity


    def hkl_labels(filename):
        """Extract hkl labels from file"""
        try:
            hkl_labels = \
            np.loadtxt(os.path.join(reference_peaks_dir, filename),
                                    dtype=np.unicode_, usecols=(2,))
        except IndexError:
            x, _ = xydata_reference(filename)
            hkl_labels = np.full_like(x, '', dtype=np.unicode_)

        return hkl_labels


    def stick_plotter(ax, label_text, twotheta, intensity, hkl_labels, color):
        """ Make a stick plot in a given axes for a given reference """
        stem_container = ax.stem(twotheta, intensity)
        stem_container.baseline.set_visible(False)
        stem_container.markerline.set_visible(False)
        stem_container.stemlines.set_color(color)
        ax.annotate(label_text, xy=(1, 1), xycoords='axes fraction',
                    xytext=(10, 0), textcoords='offset points', va='top',
                    color=color)

        if any(hkl_labels):
            ymax = max(intensity) #TODO: exclude peaks outside plotting area
            for x, y, label in zip(twotheta, intensity, hkl_labels):
                if y / ymax > 0.5:
                    xtext = x - 0.2
                    ytext = y
                    ha = 'right'; va = 'top'
                else:
                    xtext = x
                    ytext = y + 10
                    ha = 'center'; va = 'bottom'

                label = ax.annotate(label, xy=(x, y), xycoords='data',
                                    xytext=(xtext, ytext), textcoords='data',
                                    va=va, ha=ha, rotation=90, color=color)
                label.set_fontsize('xx-small')


    # Plot stick plots for references and label them
    for ax, ref, fname in zip(axs_refs, references, references_fnames):
        twotheta, intensity = xydata_reference(fname)
        hkl_lbls = hkl_labels(fname)
        style = refs_labels_style[ref]
        label_text = style['label']
        color = style['color']
        stick_plotter(ax, label_text, twotheta, intensity, hkl_lbls, color)
        ax.set(ylim=[0, 110])
        ax.tick_params(axis='y', which='both', left=False, labelleft=False)


    # Axis
    # Set up label for X axis for bottom subplot
    axs[-1].set(xlabel=r'$2\theta$, degree')
    axs[-1].xaxis.set_major_locator(MultipleLocator(10))
    axs[-1].xaxis.set_minor_locator(MultipleLocator(2))
    # No label and ticks labels for X axis for the other subplots
    for ax in axs[:-1]:
        plt.setp(ax.get_xticklabels(), visible=False)

    return fig, axs

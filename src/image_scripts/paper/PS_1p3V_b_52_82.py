"""Plot diffraction patterns 52 to 82 for experiment "b" in PS at 1.3 V"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_1p3V_b"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_1p3V_b_52_82.svg"

first_pattern = 52
last_pattern = 82
references = ['Pd', 'PdCl2', 'CuCl']
layers = {'Pd': (0, 83),
          'PdCl2': (4, 65),
          'X1+X2': (52, 70),
          'CuCl': (66, 89),
          'X3+X4': (67, 81),
          'MG': (77, 100)}
offset_patterns = 2000
excess_length = offset_patterns / 2 #for vertical lines indicating peaks


def xydata(pattern):
    """Prepare data for plotting a given pattern

    pattern : int
    out : two numpy 1D arrays

    Note: similar to sub-function "xydata" in function
    "powder_diffr_fig" and others.  Merge them and into one single
    function and place it in src/functions to un-DRY.

    """
    d = np.loadtxt(os.path.join(measured_patterns_dir, str(pattern) +
                                '.dat'))
    x, y = d[:,0], d[:,1] - offset_patterns * pattern
    return np.vstack((x, y))


def nearest_data_point(dataset, x):
    """Find the nearest data point to a given X value.

    Parameters
    ----------
    dataset: numpy array with shape (2, no of datapoints in dataset)
    x: given X value

    Returns
    -------
    index, X and Y values of data point, which is closest to
    parameter 'x'.

    """
    data_x, data_y = dataset
    nearest_idx = np.searchsorted(data_x, x)
    return nearest_idx, data_x[nearest_idx], data_y[nearest_idx]


def yval(pattern, x):
    """Return Y value of data point in pattern closest to a X value"""
    return nearest_data_point(xydata(pattern), x)[2]


def yval_max(patterns, x):
    """Return highest intensity value for given 2theta value.

    Although patterns are offset by a given value, one pattern might
    have a high peak, which goes above the pattern above it.  This
    maximum intensity value is needed to determine the top side of the
    vertical lines indicating peak positions.

    Parameters
    ----------
    patterns: list containing two integers, the first and the last
    pattern of the series of patterns to be considered
    x: float, the 2theta value for which to calculate the intensity
    value

    Returns
    -------
    yval_max: float, the maximum intensity value

    """
    st, end = patterns
    l = [yval(pattern, x) for pattern in range(st, end + 1)]
    return max(l)


fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            patterns=(first_pattern, last_pattern, 1),
                            position_subplot_measured=3,
                            reference_peaks_dir=reference_peaks_dir,
                            twotheta_range=[2.5, 21],
                            label_every_nth_pattern=5,
                            references=references,
                            offset_patterns=offset_patterns,
                            layers=layers,
                            figwidth='two_column')

fig.set_figheight(fig.get_figwidth())

# Add vertical lines indicating diffraction peaks
ax = axs[2]   # subplot containing measured diffraction patterns
offset_labels = 2 #in points

# [[2theta, [1st_pattern, last_pattern]]]
X1 = [[6.04, [52, 69]],
      [12.07, [52, 69]]]
X2 = [[2.84, [55, 73]],
      [4.03, [55, 72]],
      [4.20, [56, 71]],
      [4.95, [57, 72]],
      [5.68, [56, 72]],
      [13.47, [63, 69]]]
X3 = [[3.30, [70, 79]],
      [5.98, [69, 81]],
      [6.59, [68, 80]],
      [8.28, [67, 81]],
      [9.97, [67, 81]],
      [10.2, [67, 81]],
      [10.88, [67, 81]],
      [14.13, [68, 80]],
      [16.39, [67, 80]],
      [19.89, [68, 79]],
      [20.04, [68, 79]]]
X4 = [[3.81, [73, 82]],
      [6.21, [70, 82]]]

for peaks, color in zip((X1, X2, X3, X4), ('black', 'blue', 'red', 'green')):
    for peak in peaks:
        ax.vlines(peak[0],
                  yval(peak[1][1], peak[0]) - excess_length,
                  yval_max(peak[1], peak[0]) + excess_length,
                  linestyles='dashed', linewidths=0.5,
                  colors=color, zorder=3)

# Annotate 1st X1 peak
xann = X1[0][0]
yann = yval_max(X1[0][1], X1[0][0]) + excess_length
label = ax.annotate('X1', xy=(xann, yann), xycoords='data',
                    xytext=(0, offset_labels), textcoords='offset points',
                    ha='center', va='bottom')
#label.set_fontsize('small')

# Annotate one X2 peak
xann = X2[0][0]
yann = yval_max((first_pattern, X2[0][1][1]), X2[0][0]) + excess_length
label = ax.annotate('X2', xy=(xann, yann), xycoords='data',
                    xytext=(4, offset_labels), textcoords='offset points',
                    ha='center', va='bottom', color='blue')

# Annotate one X3 peak
text_ann = 'X3'
i_ann = 0   # index of vertical line to annotate (in its list)
x_ann = X3[i_ann][0]
y_ann = yval(X3[i_ann][1][1], X3[i_ann][0]) - excess_length
label = ax.annotate(text_ann, xy=(x_ann, y_ann), xycoords='data',
                    xytext=(0, - offset_labels), textcoords='offset points',
                    ha='center', va='top', color='red')

# Annotate one X4 peak
text_ann = 'X4'
i_ann = 0   # index of vertical line to annotate (in its list)
x_ann = X4[i_ann][0]
y_ann = yval(X4[i_ann][1][1], X4[i_ann][0]) - excess_length
label = ax.annotate(text_ann, xy=(x_ann, y_ann), xycoords='data',
                    xytext=(0, - offset_labels), textcoords='offset points',
                    ha='center', va='top', color='green')

if __name__ == "__main__":
    fig.savefig(figure_fn)

#plt.grid()
#plt.show()

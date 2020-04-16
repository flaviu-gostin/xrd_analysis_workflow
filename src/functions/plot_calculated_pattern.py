""" Plot calculated diffraction pattern

Data should be provided as 2 arrays
First array is the two-theta positions of reflections
Second array is the corresponding intensities

"""

import matplotlib.pyplot as plt


def plot_calculated_pattern(two_theta, intensity, color='black', savefile=None):
    """Plot a calculated diffraction pattern.

    Parameters
    ----------
    two_theta, intensity : 2x numpy arrays
        Tuple with two elements, both numpy arrays.  First is the 2theta values
    in degree for each reflection and second is the corresponding intensity
    values
    color : str
        Color of the bars
    savefile : str
        Filename for saving the plot ( png works).  If not provided, show plot
    in a window.

    """
    plt.stem(two_theta, intensity, linefmt=color, markerfmt='None')
    # For more advanced control of the format properties see here:
    # https://matplotlib.org/gallery/lines_bars_and_markers/stem_plot.html#sphx-glr-gallery-lines-bars-and-markers-stem-plot-py
    if not savefile:
        plt.show()
    else:
        plt.savefig(savefile, dpi=500)
        plt.close()

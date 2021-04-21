""" Calculate/plot diffraction pattern from structure """


from pymatgen import Lattice, Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator
import matplotlib.pyplot as plt


def calculate_pattern(structure, wavelength, two_theta_range):
    """
    Calculates the diffraction pattern for a structure.

    Calculates the position and intensity of Bragg peaks a given
    crystal structure would originate in a diffraction experiment
    performed with a X-ray beam of given wavelength.

    Parameters
    ----------
    structure : pymatgen Structure object
        See https://pymatgen.org/pymatgen.core.structure.html
    wavelength : str/float
        E.g. 'CuKa', 1.234 (in Angstrom)
    two_theta_range : tuple
        E.g. (0, 90), i.e. from 0 to 90 degree

    Returns
    -------
    two_theta, intensity : 2x numpy arrays
        Numpy arrays.  Two-theta in degree and intensity for each Bragg
    reflection.
    hkl_labels : list
        List of strings, one for each Bragg reflections.  Each string is a
    comma-separated sequence of 3-figures sub-strings corresponding to hkl
    indices of atomic planes that contribute to that Bragg reflection.

    References
    ----------
    http://matgenb.materialsvirtuallab.org/2013/01/01/Calculating-XRD-patterns.html
    https://pymatgen.org/pymatgen.analysis.diffraction.xrd.html

    """
    if type(wavelength) == int:
        wavelength = float(wavelength)
    calculator = XRDCalculator(wavelength)
    pattern = calculator.get_pattern(structure, two_theta_range=two_theta_range)
    two_theta, intensity = pattern.x, pattern.y


    #Extract hkl labels for each reflection
    #(one reflection can have contributions from multiple hkl planes)
    hkl_labels = []
    for reflection in pattern.hkls:
        #get the hkl tuples for each reflection
        #(a reflection may have contributions from several hkl planes)
        hkl_tuples = [refl['hkl'] for refl in reflection]
        #this variable above is a list of tuples
        #now, convert it to a list of strings
        hkl_strings = [''.join([str(i) for i in hkl_tup]) for hkl_tup
                       in hkl_tuples]
        hkl_string = ','.join(hkl_strings)
        hkl_labels.append(hkl_string)

    return two_theta, intensity, hkl_labels


def plot_calculated_pattern(two_theta, intensity):
    """ Create a stick plot of a calculated diffraction pattern.

    Parameters
    ----------
    two_theta, intensity : 2x numpy arrays
        Two-theta in degree and intensity for each Bragg reflection.
    color : str
        Color of the bars.
    savefile : str
        Filename for saving the plot ( png works).  If not provided, show plot
    in a window.

    Returns
    -------
    StemContainer
        https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.stem.html

    """
    stem_container = plt.stem(two_theta, intensity)
    stem_container.baseline.set_visible(False)
    stem_container.markerline.set_visible(False)
    return stem_container

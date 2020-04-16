""" Calculate diffraction pattern from structure """


from pymatgen import Lattice, Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator


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
    (two_theta, intensity) : 2x numpy arrays
        Tuple with two elements, both numpy arrays.  First is the 2theta values
    in degree for each reflection and second is the corresponding intensity
    values.

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

    return (two_theta, intensity)

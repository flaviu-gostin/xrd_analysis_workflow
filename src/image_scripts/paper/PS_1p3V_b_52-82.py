"""Plot diffraction patterns 52 to 82 for experiment "b" in PS at 1.3 V"""

import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_1p3V_b"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_1p3V_b_52-82.svg"

references = ['Pd', 'PdCl2', 'CuCl']

layers = {'Pd': (0, 83),
          'PdCl2': (4, 65),
          'X1+X2': (52, 70),
          'CuCl': (66, 89),
          'X3+X4': (67, 81),
          'MG': (77, 100)}


fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            patterns=(52, 82, 1),
                            position_subplot_measured=3,
                            reference_peaks_dir=reference_peaks_dir,
                            twotheta_range=[2.5, 21],
                            label_every_nth_pattern=5,
                            references=references,
                            layers=layers)


fig.savefig(figure_fn)

#plt.grid()
#plt.show()

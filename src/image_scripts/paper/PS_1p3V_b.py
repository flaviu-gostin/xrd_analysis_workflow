"""Create a powder diffraction figure"""

import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_1p3V_b"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_1p3V_b.svg"

references = ['Pd', 'PdCl2', 'CuCl']

layers = {'Pd': (0, 83),
          'PdCl2': (4, 65),
          'X1+X2': (52, 70),
          'CuCl': (66, 89),
          'X3+X4': (67, 81),
          'MG': (77, 100)}


fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            patterns=(0, 101, 2),
                            position_subplot_measured=3,
                            reference_peaks_dir=reference_peaks_dir,
                            label_every_nth_pattern=10,
                            references=references,
                            layers=layers)


fig.savefig(figure_fn)

#plt.grid()
#plt.show()

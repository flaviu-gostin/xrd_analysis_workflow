"""Create a powder diffraction figure"""

import matplotlib.pyplot as plt
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_1p3V_a"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_1p3V_a.svg"

references = ['Pd', 'PdCl2', 'CuCl']

layers = {'Pd': (4, 16),
          'PdCl2': (15, 15),
          'CuCl': (17, 17),
          'MG': (17, 20)}


fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            position_subplot_measured=3,
                            reference_peaks_dir=reference_peaks_dir,
                            label_every_nth_pattern=1,
                            offset_patterns=5000,
                            references=references,
                            layers=layers)


fig.savefig(figure_fn)

#plt.grid()
#plt.show()

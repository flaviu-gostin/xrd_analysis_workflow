"""Create a powder diffraction figure"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_0p5V_b"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_0p5V_b.svg"

patterns = (97, 102, 1)
references = ['Pd', 'CuCl', 'ZrOCl2_8H2O']
position_subplot_measured=3

fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            patterns=patterns,
                            position_subplot_measured=position_subplot_measured,
                            reference_peaks_dir=reference_peaks_dir,
                            offset_patterns=2000,
                            label_every_nth_pattern=1000,#no labels wanted
                            references=references,
                            twotheta_range=[2, 21],
                            linewidth=0.4,
                            height_ratio_measured_to_reference=5)

ax_measured = axs[position_subplot_measured -1]
ax_measured.set(ylim=[-196000, -180000])

#toplabel = ax_measured.annotate('$y = 4.671 mm', xy=)

axs[-1].xaxis.set_major_locator(MultipleLocator(5))
axs[-1].xaxis.set_minor_locator(MultipleLocator(1))

fig.savefig(figure_fn)

#plt.grid()
#plt.show()

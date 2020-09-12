"""Create a powder diffraction figure"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import sys
sys.path.append('..')
from plot_diffraction_patterns import powder_diffr_fig

measured_patterns_dir = "../../../results/intermediate/integrated_1D/PS_0p0V_a"
reference_peaks_dir = "../../../results/intermediate/peaks_references"
figure_fn = "../../../results/final/PS_0p0V_a.svg"

references = ['Pd3.97', 'Pd3.91', 'Pd', 'CuCl']
position_subplot_measured=4

#layers = {'Corrosion\nproducts': (0, 149),
#          'Metallic\nglass': (149, 167)}

fig, axs = powder_diffr_fig(measured_patterns_dir=measured_patterns_dir,
                            position_subplot_measured=position_subplot_measured,
                            reference_peaks_dir=reference_peaks_dir,
                            offset_patterns=100,
                            label_every_nth_pattern=10,#no labels wanted
                            references=references,
                            twotheta_range=[27, 36],
                            linewidth=0.3,
                            #layers=layers,
                            height_ratio_measured_to_reference=7)

ax_measured = axs[position_subplot_measured -1]
ax_measured.set(ylim=[-13500, 6500])
ax_measured.annotate('Corrosion\nproducts', xy=(1, 0.6),
                     xycoords='axes fraction',
                     xytext=(13, 0), textcoords='offset points', va='top',
                     color='black')
ax_measured.annotate('Metallic\nglass', xy=(1, 0.15),
                     xycoords='axes fraction',
                     xytext=(20, 0), textcoords='offset points', va='top',
                     color='magenta')

for i in range(3):
    ax_i = axs[i]
    ax_i.set(ylim=[0, 45])

ax_Pd = axs[2]
ax_Pd.annotate(r'$a = 3.89 \AA$', xy=(1, 0.5), xycoords='axes fraction',
               xytext=(10, 0), textcoords='offset points', va='top',
               color='blue')

ax_CuCl = axs[-1]
ax_CuCl.set(ylim=[0, 21])

#toplabel = ax_measured.annotate('$y = 4.671 mm', xy=)

axs[-1].xaxis.set_major_locator(MultipleLocator(2))
axs[-1].xaxis.set_minor_locator(MultipleLocator(0.5))

fig.savefig(figure_fn)

#plt.grid()
#plt.show()

"""Plot stacks of 1D XRD patterns"""


import matplotlib.pyplot as plt
import os
import natsort


location_data = "../../results/intermediate/integrated_1D/"
# Sub-directories where stacks to plot are
subdirs = ["PS_1p3V_b/"]
location_plots = "../../results/final/"


# Put all of the bellow in a function "plot_stack(subdir, offset, x y ranges)"?
fig_no = 0

for subdir in subdirs:
    path = location_data + subdir

    fig_no += 1
    plt.figure(fig_no, figsize=(4, 6), dpi=100)
    plt.subplot(111)
    plt.axis([2.5, 40.5, 0, 280000])
    plt.yticks([])    # Hide y ticks
    plt.ylabel("Intensity (arbitrary unit)")
    plt.xlabel("2 theta (degree)")

    offset, o = 5000, 0    # Offset each curve by values of offset
    n = 2    # Plot every n'th curve/slice
    
    for filename in natsort.natsorted(os.listdir(path), reverse=True)[::n]:
        file = path + filename
        f_no = int(filename[:-4])

        with open(file) as f:
            x = []
            y = []
            for line in f:
                if not line.startswith("#"):
                    l_str = line.split()
                    l_float = [float(i) for i in l_str]
                else:
                    continue
                x.append(l_float[0])
                y.append(l_float[1] + offset*o)
        o += 1
        
        if f_no < 15:
            col = "blue"
        elif f_no > 15 and f_no < 53:
            col = "red"
        elif f_no > 53 and f_no < 71:
            col = "black"
        elif f_no > 71 and f_no < 85:
            col = "green"
        else:
            col = "purple"

        plt.plot(x, y, color=col, linewidth=0.8)

    plt.savefig(location_plots + subdir[:-1] + ".png", dpi=500)
    # plt.show()
    plt.close()

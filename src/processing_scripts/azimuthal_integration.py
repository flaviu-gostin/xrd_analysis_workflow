"""This script performs azimuthal integration.

It takes a list of hdf files and creates a 2theta-intensity dat file for each 
slice in each hdf file.
"""


import numpy as np
import pyFAI
import h5py
import sys
import os


location_hdfs = "../../data/"
# Names of hdf files to integrate
names = ["PS_1p3V_b"]
location_results = "../../results/intermediate/integrated_1D/"
poni_file = "../../results/intermediate/calibration/Si_17.95keV.poni"


ai = pyFAI.load(poni_file)

for name in names:
    hdf_file = location_hdfs + name + ".hdf"
    file = h5py.File(hdf_file, 'r')
    dataset = file['entry/instrument/detector/data']

    result_file_dir = location_results + name
    if not os.path.exists(result_file_dir):
        os.mkdir(result_file_dir)
        
    for idx, slice in enumerate(dataset):
        result_file = result_file_dir + "/" + str(idx) + ".dat"
        ai.integrate1d(slice, 4153, unit="2th_deg", filename=result_file)

    file.close()

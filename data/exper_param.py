# These variables will be called by various Python scripts
wavelength = 0.6907e-10   # wavelength in meter
calibrant = 'Si'
detector_pixel_size = (2.53e-5, 2.53e-5)   # in meter
detector_shape = (2045, 4098)   # number of pixels


# Approximate experiment geometry
# According to pyFAI library
# See https://pyfai.readthedocs.io/en/stable/geometry.html
distance_sample_detector = 1.3e-1
poni1 = 2e-3
poni2 = 2e-3
rot1 = 0
rot2 = 0
rot3 = 0


# Several points on each diffraction ring selected manually from the calibration
# diffraction image (Si_17.95keV)
p =[]
p.append([854, 21, 0])    # [dim0 (in pixels), dim1, ring index]
p.append([854, 86, 0])
p.append([950, 527, 0])
p.append([1045, 696, 0])
p.append([1217, 902, 0])
p.append([1654, 1155, 0])
p.append([2000, 1206, 0])
p.append([66, 66, 1])
p.append([66, 134, 1])
p.append([70, 186, 1])
p.append([321, 1017, 1])
p.append([499, 1278, 1])
p.append([1110, 1774, 1])
p.append([1193, 1814, 1])
p.append([1519, 1932, 1])
p.append([1837, 1987, 1])
p.append([1926, 1991, 1])
p.append([17, 1250, 2])
p.append([33, 1268, 2])
p.append([123, 1410, 2])
p.append([734, 1994, 2])
p.append([959, 2121, 2])
p.append([1775, 2357, 2])
p.append([1904, 2366, 2])
p.append([246, 2348, 3])
p.append([672, 2616, 3])
p.append([1943, 2943, 3])
p.append([141, 2676, 4])
p.append([712, 2998, 4])
p.append([2018, 3270, 4])
p.append([112, 3290, 5])
p.append([1010, 3666, 5])
p.append([1843, 3800, 5])
p.append([127, 3666, 6])
p.append([707, 3905, 6])
p.append([1431, 4081, 6])

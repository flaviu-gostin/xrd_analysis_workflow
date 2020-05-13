# all these directories need to exist!

DATA_DIR=data
HDF_FILES=$(wildcard $(DATA_DIR)/PS*.hdf) #hdf-s need to be downloaded

RESULTS_INTERM_DIR=results/intermediate
INT_PATT_DIR=$(RESULTS_INTERM_DIR)/integrated_1D

# All integrated patterns from one hdf file go in a directory with the same name
# Need to create those directories
INT_PATT_DIRS=$(patsubst $(DATA_DIR)/%.hdf, $(INT_PATT_DIR)/%, $(HDF_FILES))

PONI_FILE=$(RESULTS_INTERM_DIR)/calibration/Si_17.95keV.poni # git add this one

SRC_DIR=src
PROC_SRC_DIR=$(SRC_DIR)/processing_scripts
IMG_SRC_DIR=$(SRC_DIR)/image_scripts
LANGUAGE=python
AZIM_INT_SRC=$(PROC_SRC_DIR)/azimuthal_integration.py
AZIM_INT_EXE=$(LANGUAGE) $(AZIM_INT_SRC)


.PHONY: all data validate eda analysis slides patch clean test verbose coverage

all:
	make data
	make analysis

data:
	mkdir data
	cd data && wget -O xrd_data.tgz https://ndownloader.figshare.com/files/14574803?private_link=5f423271a5a4e7fee3ed
	cd data && tar -zxvf xrd_data.tgz

validate:
# use hash, see project-alpha

eda:
# to do

analysis:
	cd src/processing_scripts/ && python calibration.py
	cd src/processing_scripts/ && python azimuthal_integration.py
	cd src/processing_scripts/ && python peak_calc.py
	cd src/image_scripts/ && python stack_1D.py
	cd src/image_scripts/ && python raw_diffr_images.py

calibration :
# check calibration.py and make it take dependencies from sys.arg
# so that they are given explicitly in this Makefile

.PHONY : ai-all
ai-all : $(INT_PATT_DIRS)

.PHONY : ai-test
ai-test : $(INT_PATT_DIR)/PS_1p3V_b

$(INT_PATT_DIR)/% : $(DATA_DIR)/%.hdf $(PONI_FILE) $(AZIM_INT_SRC)
	$(AZIM_INT_EXE) $(PONI_FILE) $< $@

slides:
	cd slides && make slides

patch:
	cat azimuthalIntegrator.patch | patch -d `find -name azimuthalIntegrator.py -printf %h`

clean:
# to do

RESULTS_INTERMED:=results/intermediate
PONI_FILE:=$(RESULTS_INTERMED)/Si_17.95keV.poni

SRC_DIR:=src
PROC_SRC_DIR:=$(SRC_DIR)/processing_scripts
IMG_SRC_DIR:=$(SRC_DIR)/image_scripts
LANGUAGE:=python
AI_SRC:=$(PROC_SRC_DIR)/azimuthal_integration.py
AI_EXE:=$(LANGUAGE) $(AI_SRC)
CALIB_SRC:=$(PROC_SRC_DIR)/calibration.py
CALIB_EXE:=$(LANGUAGE) $(CALIB_SRC)

.PHONY : all data validate eda analysis slides patch test verbose coverage
.PHONY : clean-all

all:
	make data
	make analysis

data:
	mkdir -p data
	cd data && wget -O xrd_data.tgz https://ndownloader.figshare.com/files/14574803?private_link=5f423271a5a4e7fee3ed
	cd data && tar -zxvf xrd_data.tgz

validate:
# use hash, see project-alpha

eda:
# to do

analysis:
	make calibration
	make ai-all
	cd src/processing_scripts/ && python peak_calc.py
	cd src/image_scripts/ && python stack_1D.py
	cd src/image_scripts/ && python raw_diffr_images.py

.PHONY : calibration clean-calibration
## calibration      : Refine experiment geometry
calibration :
	mkdir -p $(dir PONI_FILE)
	make $(PONI_FILE)

$(PONI_FILE) : $(CALIB_SRC)
	$(CALIB_EXE) $@
# todo: move variables out of calibration.py into a config file in data/
# ... and add that config file as a prerequisite to this rule

clean-calibration :
	rm -f $(PONI_FILE)


# azimuthal integration 'ai'
# these HDF variables are here because we need to first download some hdf files
HDF_DIR:=data
HDF_FILES:=$(wildcard $(HDF_DIR)/*.hdf)
HDF_STEMS:=$(basename $(notdir $(HDF_FILES)))
INT_1D_DIR:=$(RESULTS_INTERMED)/integrated_1D
# for each hdf file, create a directory with same name
INTEGRATED_DIRS:=$(addprefix $(INT_1D_DIR)/,$(HDF_STEMS))

# simpler target names for 'ai' of individual hdf files, e.g. 'ai-PS_1p3V-b'
AI_INDIVIDUAL_TARGETS:=$(addprefix ai-,$(HDF_STEMS))

.PHONY : ai-all $(AI_INDIVIDUAL_TARGETS)

## ai-all           : Perform azimuthal integration (ai) on all hdf files
ai-all : $(AI_INDIVIDUAL_TARGETS)


## ai-(hdf_stem)    : Perform 'ai' on one (hdf_stem), e.g. ai-PS_1p3V_b
$(AI_INDIVIDUAL_TARGETS) : ai-% :
	mkdir -p $(INT_1D_DIR)/$*
	make $(INT_1D_DIR)/$*/0.dat

# don't want a directory as target.  Use first file in it instead, i.e. 0.dat
$(INT_1D_DIR)/%/0.dat: $(HDF_DIR)/%.hdf $(PONI_FILE) $(AI_SRC)
	$(AI_EXE) $(PONI_FILE) $< $(patsubst %/,%,$(dir $@))

## clean-ai : Delete all directories containing integrated 1D patterns
.PHONY : clean-ai
clean-ai :
	rm -rf $(INT_1D_DIR)/*


slides:
	cd slides && make slides

patch:
	cat azimuthalIntegrator.patch | patch -d `find -name azimuthalIntegrator.py -printf %h`

clean-all:
# to do


## variables        : Print some variables
.PHONY : variables
variables :
	@echo HDF_FILES: $(HDF_FILES)
	@echo HDF_STEMS: $(HDF_STEMS)
	@echo INTEGRATED_DIRS: $(INTEGRATED_DIRS)
	@echo AI_INDIVIDUAL_TARGETS: $(AI_INDIVIDUAL_TARGETS)

## help             : Print this help
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<

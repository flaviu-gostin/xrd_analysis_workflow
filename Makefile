RESULTS_DIR:=results
RESULTS_INTERMED_DIR:=$(RESULTS_DIR)/intermediate
RESULTS_FINAL_DIR:=$(RESULTS_DIR)/final

EXPER_PARAM_FILE:=data/exper_param.py

SRC_DIR:=src
PROC_SRC_DIR:=$(SRC_DIR)/processing_scripts
IMG_SRC_DIR:=$(SRC_DIR)/image_scripts
LANGUAGE:=python
AI_SRC:=$(PROC_SRC_DIR)/azimuthal_integration.py
AI_EXE:=$(LANGUAGE) $(AI_SRC)
CALIB_SRC:=$(PROC_SRC_DIR)/calibration.py
CALIB_EXE:=$(LANGUAGE) $(CALIB_SRC)
PONI_FILE:=$(RESULTS_INTERMED_DIR)/Si_17.95keV.poni


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
	make peaks
	make tables
	cd src/image_scripts/ && python stack_1D.py
	cd src/image_scripts/ && python raw_diffr_images.py


.PHONY : calibration clean-calibration
## calibration      : Refine experiment geometry
calibration :
	mkdir -p $(dir PONI_FILE)
	make $(PONI_FILE)

$(PONI_FILE) :  $(EXPER_PARAM_FILE) $(CALIB_SRC)
	$(CALIB_EXE) $< $@

clean-calibration :
	rm -f $(PONI_FILE)


# azimuthal integration 'ai'
# these HDF variables are here because we need to first download some hdf files
HDF_DIR:=data
HDF_FILES:=$(wildcard $(HDF_DIR)/*.hdf)
HDF_STEMS:=$(basename $(notdir $(HDF_FILES)))
INT_1D_DIR:=$(RESULTS_INTERMED_DIR)/integrated_1D
# for each hdf file, create a directory with same name
INTEGRATED_DIRS:=$(addprefix $(INT_1D_DIR)/,$(HDF_STEMS))

# simpler target names for 'ai' of individual hdf files, e.g. 'ai-PS_1p3V-b'
AI_INDIVIDUAL_TARGETS:=$(addprefix ai-,$(HDF_STEMS))

.PHONY : ai-all $(AI_INDIVIDUAL_TARGETS)

## ai-all           : Perform azimuthal integration (ai) on all hdf files
ai-all : $(AI_INDIVIDUAL_TARGETS)


## ai-(hdf_stem)    : Perform 'ai' on one (hdf_stem), e.g. ai-PS_1p3V_b
$(AI_INDIVIDUAL_TARGETS) : ai-% :   #"static pattern rule"
	mkdir -p $(INT_1D_DIR)/$*
	make $(INT_1D_DIR)/$*/0.dat

# don't want a directory as target.  Use first file in it instead, i.e. 0.dat
$(INT_1D_DIR)/%/0.dat: $(HDF_DIR)/%.hdf $(PONI_FILE) $(AI_SRC)
	$(AI_EXE) $(PONI_FILE) $< $(patsubst %/,%,$(dir $@))

## clean-ai         : Delete all directories containing integrated 1D patterns
.PHONY : clean-ai
clean-ai :
	rm -rf $(INT_1D_DIR)/*


.PHONY : peaks
PEAKS_DIR:=$(RESULTS_INTERMED_DIR)/peaks
PEAKS_SRC:=$(PROC_SRC_DIR)/determine_peak_position.py
PEAKS_EXE:=$(LANGUAGE) $(PEAKS_SRC)
## peaks            : Determine peak position for selected peaks
peaks :
	mkdir -p $(PEAKS_DIR)
	make peaks-Pd113-all
#       you can add here other peaks

PEAKS_PD113_INDIVIDUAL_TARGETS:=$(addprefix peaks-Pd113-,$(HDF_STEMS))
.PHONY : peaks-Pd113-all $(PEAKS_PD113_INDIVIDUAL_TARGETS)
## peaks-Pd113-all  : Determine position of Pd113 peaks for all scans
peaks-Pd113-all : $(PEAKS_PD113_INDIVIDUAL_TARGETS)

## peaks-Pd113-(hdf_stem) : Determ pos of Pd113 peaks for given (hdf_stem)
$(PEAKS_PD113_INDIVIDUAL_TARGETS) : peaks-Pd113-% :   #"static pattern rule"
	make $(PEAKS_DIR)/$*_Pd113.dat

CONFIG_PD113:=$(SRC_DIR)/config_Pd113.py
$(PEAKS_DIR)/%_Pd113.dat : $(INT_1D_DIR)/%/0.dat $(CONFIG_PD113) $(PEAKS_SRC)
	$(PEAKS_EXE) $(dir $<) $(CONFIG_PD113) $@

.PHONY : clean-peaks
clean-peaks :
	rm -rf $(PEAKS_DIR)/*


TABLE_PD_FILE:=$(RESULTS_FINAL_DIR)/table_Pd_summary.txt
TABLE_PD_SRC:=$(SRC_DIR)/table_scripts/Pd_summary.py
TABLE_PD_EXE:=$(LANGUAGE) $(TABLE_PD_SRC)
TABLE_PD_CONFIG:=easy
FILES_FOR_TABLE_PD:=extract somehow from config file
## tables           : Create tables (todo: refactor script creating Pd table!)
.PHONY : tables
tables :
	make $(TABLE_PD_FILE)
# To do: refactor this one
$(TABLE_PD_FILE) :  $(TABLE_PD_SRC)
	cd $(dir $(TABLE_PD_SRC)) && $(LANGUAGE) $(notdir $(TABLE_PD_SRC))


slides:
	cd slides && make slides

patch:
	cat azimuthalIntegrator.patch | patch -d `find -name azimuthalIntegrator.py -printf %h`

clean-all:
	make clean-calibration
	make clean-ai
	make clean-peaks
# add other clean rules as you create them


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

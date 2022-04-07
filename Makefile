DATA_DIR:=data
EXPER_PARAM_FILE:=$(DATA_DIR)/exper_param.py
CIF_DIR:=$(DATA_DIR)/cif

RESULTS_DIR:=results
RESULTS_INTERMED_DIR:=$(RESULTS_DIR)/intermediate
RESULTS_FINAL_DIR:=$(RESULTS_DIR)/final

SRC_DIR:=src
PROC_SRC_DIR:=$(SRC_DIR)/processing_scripts
IMG_SRC_DIR:=$(SRC_DIR)/image_scripts
LANGUAGE:=python
AI_SRC:=$(PROC_SRC_DIR)/azimuthal_integration.py
AI_EXE:=$(LANGUAGE) $(AI_SRC)
CALIB_SRC:=$(PROC_SRC_DIR)/calibration.py
CALIB_EXE:=$(LANGUAGE) $(CALIB_SRC)
PONI_FILE:=$(RESULTS_INTERMED_DIR)/Si_17.95keV.poni


.PHONY : all data clean-data validate eda analysis slides clean-all

all:
	make data
	make validate
	make analysis
	make figures


data:
	cd data && make data

clean-data:
	cd data && make clean-data

validate:
	cd data && make validate

eda:
# to do

analysis:
	make calibration
	make ai-all
	make peaks
	make tables
	make reference-peaks



.PHONY : calibration calibration-check clean-calibration
## calibration      : Refine experiment geometry
calibration :
	mkdir -p $(dir $(PONI_FILE))
	make $(PONI_FILE)
	make calibration-check

$(PONI_FILE) :  $(EXPER_PARAM_FILE) $(CALIB_SRC)
	$(CALIB_EXE) $< $@

calibration-check :
	make ai-Si_17.95keV
	cd src/image_scripts/ && $(LANGUAGE) check_calibration.py

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
# don't use above rule.  Use ai-... to avoid problems with inexistent dir

## clean-ai         : Delete all directories containing integrated 1D patterns
.PHONY : clean-ai
clean-ai :
	rm -rf $(INT_1D_DIR)/*



.PHONY : peaks
PEAKS_DIR:=$(RESULTS_INTERMED_DIR)/peaks
PEAKS_SRC:=$(PROC_SRC_DIR)/determine_peak_position.py
PEAKS_EXE:=$(LANGUAGE) $(PEAKS_SRC)
PEAKS_FUNC:=$(SRC_DIR)/functions/peak_calc.py
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
$(PEAKS_DIR)/%_Pd113.dat : $(INT_1D_DIR)/%/0.dat $(CONFIG_PD113) \
$(EXPER_PARAM_FILE) $(PEAKS_SRC) $(PEAKS_FUNC)
	$(PEAKS_EXE) $(dir $<) $(CONFIG_PD113) $(EXPER_PARAM_FILE) $@

.PHONY : clean-peaks
## clean-peaks      : Delete all files containing info on on peaks
clean-peaks :
	rm -rf $(PEAKS_DIR)/*



TABLE_PD_FILE:=$(RESULTS_FINAL_DIR)/table_Pd_summary.txt
TABLE_PD_SRC:=$(SRC_DIR)/table_scripts/Pd_summary.py
TABLE_PD_EXE:=$(LANGUAGE) $(TABLE_PD_SRC)
HDF_STEMS_FOR_TABLE_PD:=PS_1p3V_b PSA_1p3V_c PSP_1p3V_b PSAP_1p3V_a PS_0p7V_b
HDF_STEMS_FOR_TABLE_PD+=PS_0p5V_b PS_0p0V_a
FILENAMES_FOR_TABLE_PD:=$(addsuffix _Pd113.dat,$(HDF_STEMS_FOR_TABLE_PD))
FILES_FOR_TABLE_PD:=$(addprefix $(PEAKS_DIR)/,$(FILENAMES_FOR_TABLE_PD))
.PHONY : tables clean-tables
## tables           : Create tables
tables :
	mkdir -p $(RESULTS_FINAL_DIR)
	make $(TABLE_PD_FILE)

$(TABLE_PD_FILE) :  $(TABLE_PD_SRC) $(FILES_FOR_TABLE_PD)
	$(TABLE_PD_EXE) $(PEAKS_DIR) $@

## clean-tables     : Delete all tables
clean-tables :
	rm -rf $(TABLE_PD_FILE)



REF_PEAKS_SRC:=$(PROC_SRC_DIR)/calc_pattern.py
REF_PEAKS_EXE:=$(LANGUAGE) $(REF_PEAKS_SRC)
REF_PEAKS_FUNC:=$(SRC_DIR)/functions/calculate_pattern.py
REF_PEAKS_DIR:=$(RESULTS_INTERMED_DIR)/peaks_references
PHONY : reference-peaks ref-peaks-internal clean-reference-peaks
reference-peaks :
	mkdir -p $(REF_PEAKS_DIR)
	make $(REF_PEAKS_DIR)/Pd.dat
	make $(REF_PEAKS_DIR)/CuCl.dat
	make $(REF_PEAKS_DIR)/PdCl2.dat
	make $(REF_PEAKS_DIR)/ZrOCl2_8H2O.dat
	make $(REF_PEAKS_DIR)/Cu.dat
	make $(REF_PEAKS_DIR)/Cu2O.dat
	make $(REF_PEAKS_DIR)/Pd3.97.dat
	make $(REF_PEAKS_DIR)/Pd3.91.dat

$(REF_PEAKS_DIR)/%.dat : $(CIF_DIR)/%.cif $(REF_PEAKS_SRC) $(REF_PEAKS_FUNC) \
$(EXPER_PARAM_FILE)
	mkdir -p $(REF_PEAKS_DIR)
	$(REF_PEAKS_EXE) $< $@

$(REF_PEAKS_DIR)/PdCl2.dat : $(DATA_DIR)/reflections_refs/PdCl2.txt
	cp $< $@

$(REF_PEAKS_DIR)/Pd3.97.dat : $(CIF_DIR)/Pd.cif $(REF_PEAKS_SRC) $(REF_PEAKS_FUNC) \
$(EXPER_PARAM_FILE)
	mkdir -p $(REF_PEAKS_DIR)
	$(REF_PEAKS_EXE) $< $@ 3.97

$(REF_PEAKS_DIR)/Pd3.91.dat : $(CIF_DIR)/Pd.cif $(REF_PEAKS_SRC) $(REF_PEAKS_FUNC) \
$(EXPER_PARAM_FILE)
	mkdir -p $(REF_PEAKS_DIR)
	$(REF_PEAKS_EXE) $< $@ 3.91

clean-reference-peaks :
	rm -rf $(REF_PEAKS_DIR)



FIGS_SRC_DIR:=$(SRC_DIR)/image_scripts/paper
FIGS:=PS_1p3V_a PS_1p3V_b PS_0p5V_b PS_0p0V_a_interface PS_0p0V_a \
      PS_0p0V_a_heatmap PS_0p5V_b_heatmap \
      PS_1p3V_b_raw_2D PS_1p3V_b_52_82
FIGS_SRC_FNAMES:=$(addsuffix .py,$(FIGS))
FIGS_SRC_DIR:=$(IMG_SRC_DIR)/paper/
FIGS_SRC:=$(addprefix $(FIGS_SRC_DIR),$(FIGS_SRC_FNAMES))
FIGS_FNAMES:=$(addsuffix .svg,$(FIGS))
FIGS_FILES:=$(addprefix $(RESULTS_FINAL_DIR)/,$(FIGS_FNAMES))
.PHONY : figures clean-figures
## figures          : Generate figures for paper
figures : $(FIGS_FILES)

$(FIGS_FILES) : $(RESULTS_FINAL_DIR)/%.svg : $(IMG_SRC_DIR)/paper/%.py \
$(IMG_SRC_DIR)/plot_diffraction_patterns.py
	cd $(FIGS_SRC_DIR) && $(LANGUAGE) $(notdir $<)

## clean-figures    : Delete figures for paper
clean-figures :
	for file in $(FIGS_FILES); do rm -rf $$file; done



slides:
	cd slides && make slides




clean-all:
	make clean-data
	make clean-calibration
	make clean-ai
	make clean-peaks
	make clean-tables
	make clean-reference-peaks
	make clean-figures
# add other clean rules as you create them



.PHONY : venv requirements patches clean-venv
## venv             : Create virtual environment
venv :
	python3 -m venv venv

## requirements     : Install requirements (do it in a virtual environment?)
requirements :
	python -m pip install -r requirements.txt

pyFAI_bad_ver:=0.17.0

patches :
#	no need for patches for now

## clean-venv       : Delete virtual environment
clean-venv :
	rm -rf venv



.PHONY : test clean-test
## test             : Execute some rules using test files
test :
	make ai-all 'HDF_DIR:=data/test_data' #overriding variable
	make peaks 'HDF_DIR:=data/test_data'
	make tables 'HDF_STEMS_FOR_TABLE_PD:=test-PS_1p3V_b test-PSP_1p3V_b'
# add more rules as you create them

## clean-test       : Delete files created by `make test`
clean-test :
	rm -rf $(INT_1D_DIR)/test*
	rm -rf $(PEAKS_DIR)/test*
	make clean-tables



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

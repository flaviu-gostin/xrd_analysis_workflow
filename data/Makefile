TEST_DATA_DIR:=test_data
TEST_FILES:=$(addprefix  $(TEST_DATA_DIR)/test-,PS_1p3V_b.hdf PSP_1p3V_b.hdf)

# hdf files larger than 200M
HDF200:=PS_0p0V_a.hdf PS_0p5V_b.hdf PS_0p7V_b.hdf PS_1p3V_b.hdf PSA_1p3V_c.hdf
HDF200+=PSP_1p3V_b.hdf PSA_1p3V_a.hdf PS_1p3V_c.hdf PSAP_1p3V_a.hdf
HDF200+=PSP_1p3V_a.hdf PSAP_1p3V_d.hdf PS_0p7V_a.hdf PSA_1p3V_d.hdf
HDF200+=PSAP_1p3V_c.hdf PSAP_1p3V_b.hdf PS_1p3V_a.hdf PSA_1p3V_b.hdf
ARCHIVES=$(wildcard PS*V.tgz) # Don't use `:=` here.  Using `=`, this variable
#is expanded when it's substituted, i.e. after PS*V.tgz are downloaded (before
#download, there is no PS*V.tgz file).  See:
#https://www.gnu.org/software/make/manual/html_node/Flavors.html#Flavors

.PHONY: data validate clean-data
## data             : Download data and concatenate split files
data:
	wget -i urls_Zenodo.txt
	for HDF in ${HDF200}; do cat $${HDF}_* > $${HDF}; done
	for ARCHIVE in ${ARCHIVES}; do tar -xvzf $${ARCHIVE}; done

## validate         : Check hashes of .hdf and .nxs files
validate:
	md5sum --ignore-missing --quiet -c hashes.md5

## clean-data       : Delete splits of large .hdf files and .tgz archives
clean-data:
	for HDF in ${HDF200}; do rm -f $${HDF}_*; done
	rm -rf ${ARCHIVES}

.PHONY : test-data clean-test-data
$(TEST_DATA_DIR)/test-%.hdf : %.hdf
	python generate_test_data.py $< $@

## test-data        : Generate test data
test-data : $(TEST_FILES)

$(TEST_FILES) : | $(TEST_DATA_DIR) #order-only prerequisite

$(TEST_DATA_DIR) :
	mkdir -p $(TEST_DATA_DIR)

## clean-test-data  : Delete test data
clean-test-data :
	rm -rf $(TEST_DATA_DIR)/*


## help             : Print this help
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<

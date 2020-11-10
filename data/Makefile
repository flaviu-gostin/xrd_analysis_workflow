TEST_DATA_DIR:=test_data
TEST_FILES:=$(addprefix  $(TEST_DATA_DIR)/test-,PS_1p3V_b.hdf PSP_1p3V_b.hdf)

# hdf files larger than 200M
HDF200:=PS_0p0V_a.hdf PS_0p5V_b.hdf PS_0p7V_b.hdf PS_1p3V_b.hdf PSA_1p3V_c.hdf PSP_1p3V_b.hdf PSA_1p3V_a.hdf PS_1p3V_c.hdf PSAP_1p3V_a.hdf PSP_1p3V_a.hdf PSAP_1p3V_d.hdf PS_0p7V_a.hdf PSA_1p3V_d.hdf PSAP_1p3V_c.hdf PSAP_1p3V_b.hdf PS_1p3V_a.hdf PSA_1p3V_b.hdf

.PHONY: data validate clean-splits
## data             : Download data and concatenate split files
data:
	wget -i urls_Zenodo.txt
	for HDF in ${HDF200}; do cat $${HDF}_* > ${HDF200}; done

## validate         : Check hashes of .hdf and .nxs files
validate:
	md5sum --ignore-missing --quiet -c hashes.md5

## clean-splits     : Delete splits of large .hdf files
clean-splits:
	for HDF in ${HDF200}; do rm -f $${HDF}_*; done


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

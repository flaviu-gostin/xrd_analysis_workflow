TEST_DATA_DIR:=test_data
TEST_FILES:=$(addprefix  $(TEST_DATA_DIR)/test-,PS_1p3V_b.hdf PSP_1p3V_b.hdf)

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

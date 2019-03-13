.PHONY: all data validate eda analysis slides clean test verbose coverage

all:
	make data
	make analysis

data:
	cd data && wget -O xrd_data.tgz https://ndownloader.figshare.com/files/14574803?private_link=5f423271a5a4e7fee3ed
	cd data && tar -zxvf xrd_data.tgz

validate:
	use hash, see project-alpha

eda:
	to do

analysis:
	cd src/processing_scripts/ && python calibration.py
	cd src/processing_scripts/ && python azimuthal_integration.py
	cd src/processing_scripts/ && python peak_calc.py
	cd src/image_scripts/ && python stack_1D.py
	cd src/image_scripts/ && python raw_diffr_images.py

slides:
	cd slides && make slides

clean:
	to do

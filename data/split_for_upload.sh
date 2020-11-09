#! bin/bash

# Usage: bash split_for_upload.sh


# split the file into 200M pieces for upload (errors for larger files on Zenodo)
split -b 200M ${1} ${1}_

# calculate the md5 for the file and its pieces for later checking
# also for the .nxs file
for FILE in ${1}*
do
    md5sum $FILE >> ${1}.md5
done

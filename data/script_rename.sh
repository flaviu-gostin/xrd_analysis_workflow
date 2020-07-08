#! bin/bash
# Rename xrd scan files from their original names containing a 5-figures scan number to new names containing the elctrolyte and potential as indicated in scan_numbers.txt
# Usage: bash script_rename.sh FILES_TO_RENAME

for f in "$@"
do
    extension=${f:(-4):4}
    scan_number=$(echo $f | grep -oE [0-9]{5} )
    new_bare_filename=$(grep $scan_number scan_numbers.txt | cut -d ' ' -f 1 )
    new_filename=$new_bare_filename$extension
    mv -T "$f" "$new_filename"
done

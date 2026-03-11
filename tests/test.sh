#!/bin/bash
set -e

# test folders
FOLDER_TEST=tests
FOLDER_OUT=$FOLDER_TEST/outputs
FOLDER_EXPECTED_OUT=$FOLDER_TEST/expected_outputs

clean_test_results() {
        rm -f $FOLDER_OUT/*.sh
}

get_diff_out_vs_expected() {
        diff $_out $_expct | wc -l
}

# the test
do_tests() {
        # list the content of duckyScript test folder
        ls $FOLDER_TEST/*.txt | while read _duckyscript; do
                # some useful filename vars 
                _filename="${_duckyscript##*/}"
                _filenamewe="${_filename%.*}"
                _out=$FOLDER_OUT/${_filenamewe}_out.sh

                # convert DuckyScripts to ydotool output ones
                python flipper0badusb_test.py $_duckyscript $_out silence

                # more useful filenames
                _expct=$FOLDER_EXPECTED_OUT/expected_${_filenamewe}_out.sh

                # compare output with the expected ones
                _res=$(get_diff_out_vs_expected $_out $_expct) 

                # compare and exit if there is differences
                if [ $((_res)) -eq 0 ]; then
                        echo "[OK] $_duckyscript and $_expct"
                else
                        echo "[NOK] $_duckyscript and $_expct"
                        diff $_out $_expct
                        exit 1
                fi
        done
}

mkdir -p $FOLDER_OUT/
clean_test_results
do_tests
clean_test_results


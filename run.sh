#!/bin/bash

# Description: Executes all Python scripts in the current directory.

# Ensure the script is executable: chmod +x run_all_py_scripts.sh
# Run the script: ./run_all_py_scripts.sh
clear
for script in *.py; do
    if [[ -f "$script" ]]; then
        #echo "Running: $script"
        python3 "$script"
        #echo "Finished: $script"
        #echo "-------------------"
    else
        echo "No Python scripts found in the directory."
    fi
done
,

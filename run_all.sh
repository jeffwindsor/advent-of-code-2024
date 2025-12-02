#!/usr/bin/env bash

clear
for script in *.py; do
  if [[ -f "$script" ]]; then
    python3 "$script"
  else
    echo "No Python scripts found in the directory."
  fi
done

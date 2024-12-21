#!/bin/bash

# Root directory to start searching
ROOT_DIR="."
# Target directory for storing the renamed files
TARGET_DIR="./data"

# Ensure the target directory exists
mkdir -p "$TARGET_DIR"

# Loop through subdirectories starting with "day"
find "$ROOT_DIR" -type d -name "day*" | while read -r SUBDIR; do
  # Extract the prefix (text after "day")
  PREFIX=$(basename "$SUBDIR" | sed 's/^day//')

  # Loop through files without extensions in the current subdirectory
  find "$SUBDIR" -maxdepth 1 -type f ! -name "*.*" | while read -r FILE; do
    # Get the base name of the file
    FILENAME=$(basename "$FILE")
    # Construct the new filename and move the file
    NEW_FILENAME="${PREFIX}_${FILENAME}"
    mv "$FILE" "$TARGET_DIR/$NEW_FILENAME"
    echo "Moved: $FILE -> $TARGET_DIR/$NEW_FILENAME"
  done
done


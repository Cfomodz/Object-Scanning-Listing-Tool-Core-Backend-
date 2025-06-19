#!/bin/bash

# Create a ZIP file with only the specified codebase files
ZIP_NAME="codebase_$(date +%Y%m%d_%H%M%S).zip"

echo "Creating ZIP file: $ZIP_NAME"

# Create the ZIP file with specified files and directories using 7z
7z a "$ZIP_NAME" \
  test_core.py \
  test_app.py \
  run_tests.sh \
  requirements.txt \
  build_docker.sh \
  Dockerfile \
  app.py \
  core/ \
  -x!'plugins/*' \
  -x!'*/__pycache__/*' \
  -x!'*/*.pyc' \
  -x!'*/tmp/*' \
  -x!'*/venv/*' \
  -x!'*/.env' \
  -x!'*/.git/*' \
  -x!'*/__pycache__/*' \

# Check if .dockerignore exists and add it if it does
if [ -f ".dockerignore" ]; then
  7z a "$ZIP_NAME" .dockerignore
  echo "Added .dockerignore to ZIP"
else
  echo "Warning: .dockerignore not found in current directory"
fi

echo "ZIP file created successfully: $ZIP_NAME"
echo "Contents:"
7z l "$ZIP_NAME" | head -30

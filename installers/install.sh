#!/bin/bash

# Variables - modify these as needed
REPO_URL="https://github.com/connor33341/aerovector/archive/refs/heads/master.zip"
ZIP_FILE="repo.zip"
EXTRACT_DIR="repo"
SCRIPT_TO_RUN="aerovector-master/installers/configure.sh"

# Function to handle errors
handle_error() {
    echo "$1"
    exit 1
}

# Download the repository
echo "Downloading AeroVector"
curl -L -o "$ZIP_FILE" "$REPO_URL" || handle_error "Failed to download the repository."

# Unzip the repository
echo "Unzipping AeroVector"
unzip "$ZIP_FILE" -d "$EXTRACT_DIR" || handle_error "Failed to unzip the repository."

# Run the batch file located in the repository
echo "Running configure.sh"
wine "$EXTRACT_DIR/$SCRIPT_TO_RUN" || handle_error "Failed to run the script."

# Clean up
echo "Cleaning up"
rm "$ZIP_FILE"
rm -rf "$EXTRACT_DIR"

echo "Done"

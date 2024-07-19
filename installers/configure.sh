#!/bin/bash

# Function to handle errors
handle_error() {
    echo "$1"
    exit 1
}

# Check if python is available
echo "Configuring AeroVector"
if command -v python3 &> /dev/null
then
    echo "Running Python3 as Python"
    python3 -m pip install -r requirements.txt || handle_error "Failed to install requirements"
    exit 0
fi

# Check if python is available as python (might be python2 in some systems)
if command -v python &> /dev/null
then
    echo "Running Python as Python"
    python -m pip install -r requirements.txt || handle_error "Failed to install requirements"
    exit 0
fi

# No python
handle_error "Check if python3 is installed, or check if python is in path. To download python visit https://python.org"

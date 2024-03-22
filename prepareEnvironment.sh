#!/bin/bash

# Function to check and create venv folder
check_and_create_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating 'venv' folder..."
        virtualenv venv
    fi
}

# Function to check and install virtualenv
check_and_install_virtualenv() {
    if ! command -v virtualenv &> /dev/null; then
        echo "Installing virtualenv..."
        pip install virtualenv
    fi
}

# Main function
main() {
    check_and_create_venv
    check_and_install_virtualenv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual environment and required packages set up for project."
    echo "Enter \"deacticate\" to get out of virtual environment"
}

# Run main function
main

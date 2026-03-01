#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Environment Setup..."

# 1. Setup Python Environment (Conda)
echo "Checking Conda installation..."
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Miniconda or Anaconda."
    exit 1
fi

echo "Updating/Creating Conda environment 'ai-newsletter' from env/environment.yml..."
conda env update --file env/environment.yml --prune

# 2. Setup JavaScript Environment (NPM)
echo "Checking NPM installation..."
if ! command -v npm &> /dev/null
then
    echo "NPM could not be found. Please install Node.js and NPM."
    exit 1
fi

echo "Installing NPM dependencies from env/package.json..."
# Change to the env directory to install dependencies defined in env/package.json
cd env
npm install
cd ..

echo ""
echo "Setup complete! ✅"
echo "To run python scripts, use: conda run -n ai-newsletter --no-capture-output python <script.py>"

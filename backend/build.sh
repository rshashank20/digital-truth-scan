#!/bin/bash
echo "Setting up Python environment..."
python3.11 --version
pip3 install --upgrade pip
pip3 install -r requirements.txt
echo "Build completed successfully!"

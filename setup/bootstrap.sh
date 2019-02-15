#!/bin/bash

export PATH=~/anaconda3/bin:$PATH

# Change permissions on run file
chmod u+x ../run.py
chmod u+x ./app/*

# Create an environment
conda create --name venv3 pandas flask

# Activate environment
source activate venv3

# Request info from URL - used for scraping.
conda install requests

# Boto3 allows for interaction with Python between Amazon Web Services
conda install boto3

# Install Python3
sudo apt install python3


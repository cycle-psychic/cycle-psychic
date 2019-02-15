#!/bin/bash

# Create an environment
conda create --name venv3 pandas flask

# Activate environment
source activate venv3

# Request info from URL - used for scraping.
conda install requests

# Boto3 allows for interaction with Python between Amazon Web Services
conda install boto3

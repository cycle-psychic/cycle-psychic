#!/bin/bash

# Install Anaconda
wget 'https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh'

# Create an environment
conda create --name venv3 pandas flask

# Activate environment
source activate venv3

# Request info from URL - used for scraping.
conda install requests

# Boto3 allows for interaction with Python between Amazon Web Services
conda install boto3

# Setup of folder structure
mkdir src
cd src
mkdir cyclePsychic
mkdir cyclePsychic/app
mkdir cyclePsychic/static
mkdir cyclePsychic/templates
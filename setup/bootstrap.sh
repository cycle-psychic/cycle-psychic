#!/bin/bash

export PATH=~/anaconda3/bin:$PATH

# Change permissions on run file
chmod u+x ../run.py
chmod u+x ../app/*
chmod u+x ../scrape/*

# Create an environment
conda create --name venv3 pandas flask

# Activate environment
source activate venv3

# Request info from URL - used for scraping.
conda install requests

# Boto3 allows for interaction with Python between Amazon Web Services
conda install boto3

# Install Python3
conda install python3

# Install mysql connector
conda install -c anaconda mysql-connector-python

# Install jsonify
conda install jsonify

# Install requirements for data analysis
conda install pandas

conda install numpy

conda install matplotlib

conda install seaborn

# Install scikit learn for machine learning

conda install scikit-learn

# Pip install mysql-connector-python for cross-platform compatability issues during development.
pip install mysql-connector-python==8.0.15


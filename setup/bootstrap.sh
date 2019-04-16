#!/bin/bash

export PATH=~/anaconda3/bin:$PATH

# Change permissions on run file
chmod u+x ../run.py
chmod u+x ../app/*
chmod u+x ../scrape/*

# Install Python3
conda install python3

# Install requirements for data analysis
conda install seaborn

# Install packages from requirements
conda install --yes --file requirements.txt

# update sci-kit learn
conda update scikit-learn

# upgrade pip
pip install --upgrade pip

# install mysql connector 
pip install mysql-connector-python
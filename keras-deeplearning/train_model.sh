#!/bin/bash -xe

unzip -o ../LoanStats3d_securev1.csv.zip -d .
python ../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv

# Lengthy timeout here should cover the training time on p2.xlarge
jupyter nbconvert --ExecutePreprocessor.timeout=2400 --execute lending-club-loan-grades.ipynb

# TODO:
# Send trained model and HTML output to S3

# Delete the stack that created this instance
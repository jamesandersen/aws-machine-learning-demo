#!/bin/bash -xe

unzip -o ../LoanStats3d_securev1.csv.zip -d .
python ../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv

# Lengthy timeout here should cover the training time on p2.xlarge
jupyter nbconvert --ExecutePreprocessor.timeout=2400 --execute lending-club-loan-grades.ipynb

# Send trained model and HTML output to S3
DATE=`date -u +%FT%H_%M`
aws s3 cp lc_model.h5 s3://um-aws-machine-learning-demo/$DATE/lc_model.h5
aws s3 cp lending-club-loan-grades.html s3://um-aws-machine-learning-demo/$DATE/lending-club-loan-grades.html
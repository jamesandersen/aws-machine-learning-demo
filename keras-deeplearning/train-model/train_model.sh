#!/bin/bash -xe

# Change working directory to repo
cd "${0%/*}"

# Check Keras Backend
# pip3 -q install 'keras==2.0.6' --force-reinstall
python3 -c "import keras; print(keras.backend.backend())"
logger "Keras appears to be working!"

# Fetch raw data
aws s3 cp s3://um-aws-machine-learning-demo/LoanStats3d_securev1.csv.zip .

# extract raw data
unzip -o LoanStats3d_securev1.csv.zip -d .

# generate cleaned data file for model training
python3 ../../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv

# train and save model
python3 train_model.py

# Send trained model to S3
DATE=`date -u +%FT%H_%M`
aws s3 cp output/ s3://um-aws-machine-learning-demo/$DATE/ --recursive --storage-class REDUCED_REDUNDANCY
aws s3 cp /tmp/workload.log s3://um-aws-machine-learning-demo/$DATE/workload.log --storage-class REDUCED_REDUNDANCY
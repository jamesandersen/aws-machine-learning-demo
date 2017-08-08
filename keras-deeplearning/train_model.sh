#!/bin/bash -xe

# load environment as though interactive login
#source /etc/profile.d/aml_ami.sh

# Change working directory to repo
cd "${0%/*}"

# Update Keras
#sudo pip3 install keras --upgrade --no-deps

# Check Keras Backend
python3 -c "import keras; print(keras.backend.backend())"
logger "Keras appears to be working!"

# extract data
unzip -o ../LoanStats3d_securev1.csv.zip -d .

# clean data
python3 ../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv

# train and save model
python3 train_model.py

# Send trained model to S3
DATE=`date -u +%FT%H_%M`
aws s3 cp lc_model.h5 s3://um-aws-machine-learning-demo/$DATE/lc_model.h5
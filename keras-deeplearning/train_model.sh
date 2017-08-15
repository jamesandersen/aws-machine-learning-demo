#!/bin/bash -xe

# Change working directory to repo
cd "${0%/*}"

# Check Keras Backend
python3 -c "import keras; print(keras.backend.backend())"
logger "Keras appears to be working!"

# extract raw data
unzip -o ../LoanStats3d_securev1.csv.zip -d .

# generate cleaned data file for model training
python3 ../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv

# train and save model
python3 train_model.py

# Send trained model to S3
DATE=`date -u +%FT%H_%M`
aws s3 cp lc_model.h5 s3://um-aws-machine-learning-demo/$DATE/lc_model.h5
aws s3 cp x_test.csv s3://um-aws-machine-learning-demo/$DATE/x_test.csv
aws s3 cp y_test.csv s3://um-aws-machine-learning-demo/$DATE/y_test.csv
aws s3 cp y_pred.csv s3://um-aws-machine-learning-demo/$DATE/y_pred.csv
aws s3 cp /tmp/workload.log s3://um-aws-machine-learning-demo/$DATE/workload.log
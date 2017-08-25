"""AWS Lambda Handler for making loan grade predictions"""

import os
import boto3
import botocore

# Silence warnings about TF CPP compilation flags e.g.
# "The TensorFlow library wasn't compiled to use SSE4.1 instructions, but
# these are available on your machine and could speed up CPU computations."
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import json
import numpy as np
from keras.models import load_model
from keras import backend as K

BUCKET_NAME = os.environ["bucket"]
MODEL_KEY = os.environ["modelkey"]

s3 = boto3.resource('s3')
loan_grade_model = None

# One-time per lambda instance, load the model from S3
try:
    s3.Bucket(BUCKET_NAME).download_file(MODEL_KEY, '/tmp/model.h5')
    print("Model downloaded from s3://{}/{}".format(BUCKET_NAME, MODEL_KEY))
    loan_grade_model = load_model('/tmp/model.h5')
    print("Model loaded from s3://{}/{}".format(BUCKET_NAME, MODEL_KEY))
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The {}/{} does not exist.".format(BUCKET_NAME, MODEL_KEY))
    else:
        raise

idx_to_grade = lambda x: "ABCDEFG"[x]

def sample_predict(event, context):
    #print(event['requestContext'])
    body = json.loads(event['body'])
    x = np.matrix([list(each.values()) for each in body])
    print("Received loan input data with shape {}".format(x.shape))
    pred = loan_grade_model.predict(x)
    max_indices = np.argmax(pred, axis=1)
    print(max_indices)
    grades = [idx_to_grade(x) for x in max_indices]
    response = {}
    response['statusCode'] = 200
    response['headers'] = { "X-tensorflow-prediction": "True" }
    response['body'] = json.dumps(grades)
    return response
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

#x_test = np.genfromtxt("x_test.csv", delimiter=",")
#loan_grade_model = load_model('lc_model_local.h5')
#y_pred = np.genfromtxt("y_pred.csv", delimiter=",")

#print("Making sample prediction using {} rows and {} columns".format(x_test.shape[0], x_test.shape[1]))
#pred = loan_grade_model.predict(x_test)

#if np.allclose(y_pred, pred):
#    print("Model recreated and results validated with previous predictions")
#else:
#    print("Model recreated but predictions are inconsistent with previous run")
#    print("Saved Pred\t\tCurrent Pred")
#    for i in range(10):
#        print("{}\t\t{}".format(y_pred[i:i], pred[i:i]))




idx_to_grade = lambda x: "ABCDEFG"[x]

def sample_predict(event, context):
    print(event['requestContext'])
    body = json.loads(event['body'])
    x = np.matrix([list(each.values()) for each in body])
    print(x.shape)
    pred = loan_grade_model.predict(x)
    max_indices = np.argmax(pred, axis=1)
    print(max_indices)
    grades = [idx_to_grade(x) for x in max_indices]
    response = {}
    response['statusCode'] = 200
    response['headers'] = { "X-tensorflow-prediction": "True" }
    response['body'] = json.dumps(grades)
    return response

if __name__ == "__main__":
    sample_context = { "function_name": "CLI Test" }
    sample_event = { "foo": "bar"}
    grades = sample_predict(sample_context, sample_event)
    print(grades)
    K.clear_session() # https://github.com/tensorflow/tensorflow/issues/3388
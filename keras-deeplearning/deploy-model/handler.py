"""AWS Lambda Handler for making loan grade predictions"""

import os
import numpy as np

# Silence warnings about TF CPP compilation flags e.g.
# "The TensorFlow library wasn't compiled to use SSE4.1 instructions, but
# these are available on your machine and could speed up CPU computations."
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from keras.models import load_model
from keras import backend as K

x_test = np.genfromtxt("x_test.csv", delimiter=",")
loan_grade_model = load_model('lc_model_local.h5')
y_pred = np.genfromtxt("y_pred.csv", delimiter=",")

print("Making sample prediction using {} rows and {} columns".format(x_test.shape[0], x_test.shape[1]))
pred = loan_grade_model.predict(x_test)

if np.allclose(y_pred, pred):
    print("Model recreated and results validated with previous predictions")
else:
    print("Model recreated but predictions are inconsistent with previous run")
    print("Saved Pred\t\tCurrent Pred")
    for i in range(10):
        print("{}\t\t{}".format(y_pred[i:i], pred[i:i]))

idx_to_grade = lambda x: "ABCDEFG"[x]

def sample_predict(event, context):
    pred = loan_grade_model.predict(x_test)
    max_indices = np.argmax(pred, axis=1)
    print(max_indices)
    grades = [idx_to_grade(x) for x in max_indices]
    return grades

if __name__ == "__main__":
    sample_context = { "function_name": "CLI Test" }
    sample_event = { "foo": "bar"}
    grades = sample_predict(sample_context, sample_event)
    print(grades)
    K.clear_session() # https://github.com/tensorflow/tensorflow/issues/3388
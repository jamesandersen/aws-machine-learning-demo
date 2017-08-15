"""Trains neural net for Lending Club dataset and saves the results"""

import os

# Silence warnings about TF CPP compilation flags e.g.
# "The TensorFlow library wasn't compiled to use SSE4.1 instructions, but
# these are available on your machine and could speed up CPU computations."
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
from keras import backend as K
import train_util as util
from model_definition import create_model

helper = util.LendingClubModelHelper()

# Read in lending club data 
helper.read_csv("lc-2015-loans.csv", 
                util.APPLICANT_NUMERIC +
                util.APPLICANT_CATEGORICAL +
                util.CREDIT_NUMERIC +
                util.LABEL)

# Divide the data set into training and test sets
helper.split_data(util.APPLICANT_NUMERIC + util.CREDIT_NUMERIC,
                  util.APPLICANT_CATEGORICAL,
                  util.LABEL,
                  test_size=0.2,
                  row_limit = os.environ.get("sample"))

helper.train_model(create_model, True)

output = 'output/'
if not os.path.exists(output):
    os.makedirs(output)
helper.model.save("{}lc_model.h5".format(output))  # creates a HDF5 file 'lc_model.h5'
np.savetxt("{}x_test.csv".format(output), helper.x_test[:100].as_matrix(), delimiter=',')
np.savetxt("{}y_test.csv".format(output), helper.y_test[:100].as_matrix(), delimiter=',')
y_pred = helper.model.predict(helper.x_test[:100].as_matrix())
np.savetxt("{}y_pred.csv".format(output), y_pred, delimiter=',')

K.clear_session() # https://github.com/tensorflow/tensorflow/issues/3388

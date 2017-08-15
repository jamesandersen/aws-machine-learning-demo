"""Trains neural net for Lending Club dataset and saves the results"""

import os
import numpy as np
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

helper.model.save('lc_model.h5')  # creates a HDF5 file 'lc_model.h5'
np.savetxt('x_test.csv', helper.x_test[:100].as_matrix(), delimiter=',')
np.savetxt('y_test.csv', helper.y_test[:100].as_matrix(), delimiter=',')
y_pred = helper.model.predict(helper.x_test[:100].as_matrix())
np.savetxt('y_pred.csv', y_pred, delimiter=',')


"""Trains neural net for Lending Club dataset and saves the results"""

import os

# Silence warnings about TF CPP compilation flags e.g.
# "The TensorFlow library wasn't compiled to use SSE4.1 instructions, but
# these are available on your machine and could speed up CPU computations."
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import pandas as pd
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

# Save confusion matrix
import seaborn as sns
from sklearn.metrics import confusion_matrix, f1_score

y_pred = helper.model.predict(helper.x_test.as_matrix())
y_pred_classes = pd.DataFrame((y_pred.argmax(1)[:,None] == np.arange(y_pred.shape[1])), \
                                columns=helper.y_test.columns, \
                                index=helper.y_test.index)
y_test_vals = helper.y_test.idxmax(1)
y_pred_vals = y_pred_classes.idxmax(1)
f1 = f1_score(y_test_vals, y_pred_vals, average='weighted')
print("Test Set Accuracy: {:.00%}".format(f1))

cfn_matrix = confusion_matrix(y_test_vals, y_pred_vals)
cfn_frame = pd.DataFrame(cfn_matrix, index=helper.y_test.columns, columns=helper.y_test.columns)
hm = sns.heatmap(cfn_frame, square=True, cmap=sns.color_palette("Blues", 30), annot=cfn_matrix, fmt='g')
figure = hm.get_figure()    
figure.savefig("{}confusion_matrix.png".format(output), dpi=400)

K.clear_session() # https://github.com/tensorflow/tensorflow/issues/3388

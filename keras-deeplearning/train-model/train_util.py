"""Utility logic for handling data set"""

import pandas as pd
from sklearn.model_selection import train_test_split

APPLICANT_NUMERIC = ['annual_inc', 'dti', 'age_earliest_cr', 'loan_amnt', 'installment']
APPLICANT_CATEGORICAL = ['application_type', 'emp_length', 'home_ownership', 'addr_state', 'term']
CREDIT_NUMERIC = ['acc_now_delinq', 'acc_open_past_24mths', 'avg_cur_bal', 'bc_open_to_buy',
                  'bc_util', 'delinq_2yrs', 'delinq_amnt', 'fico_range_high', 'fico_range_low',
                  'last_fico_range_high', 'last_fico_range_low', 'open_acc', 'pub_rec', 'revol_util',
                  'revol_bal', 'tot_coll_amt', 'tot_cur_bal', 'total_acc', 'total_rev_hi_lim',
                  'num_accts_ever_120_pd', 'num_actv_bc_tl', 'num_actv_rev_tl', 'num_bc_sats',
                  'num_bc_tl', 'num_il_tl', 'num_rev_tl_bal_gt_0', 'pct_tl_nvr_dlq',
                  'percent_bc_gt_75', 'tot_hi_cred_lim', 'total_bal_ex_mort', 'total_bc_limit',
                  'total_il_high_credit_limit', 'total_rev_hi_lim', 'all_util', 'loan_to_income',
                  'installment_pct_inc', 'il_util', 'il_util_ex_mort', 'total_bal_il', 'total_cu_tl']
LABEL = ['grade']

class LendingClubModelHelper:
    """Provides utility functions for training data"""
    def __init__(self):
        self.lcdata = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.model = None

    def read_csv(self, filename, columns):
        """Read in lending club data"""

        # ...skip the columns we're not going to use to preserve memory
        self.lcdata = pd.read_csv(filename, usecols=columns)

        # Set an ordering on our grade category so order of grades doesn't appear randome in graphs
        grade_categories = [g for g in "ABCDEFG"]
        self.lcdata["grade"] = self.lcdata["grade"].astype("category", categories=grade_categories, ordered=True)

        # Sanity check that we're working with cleaned data
        bad_rows = self.lcdata.isnull().T.any().T.sum()
        if bad_rows > 0:
            print("Rows with null/NaN values: {}".format(bad_rows))
            print("Columns with null/NaN values:")
            print(pd.isnull(self.lcdata).sum() > 0)
            print("Dropping bad rows...")
            self.lcdata.dropna(axis=0, how='any', inplace=True)
            print("Rows with null/NaN values: {}".format(self.lcdata.isnull().T.any().T.sum()))

    def split_data(self, continuous_cols, categorical_cols, label_col, test_size=0.2, row_limit=None):
        """Divide the data in to X and y dataframes and train/test split"""

        # When requested, limit the amount of data that will be used
        # Using entire data set can be painfully slow without a GPU!
        if row_limit != None:
            print("Using only a sample of {} observations".format(row_limit))
            data = self.lcdata.sample(int(row_limit))
        else:
            print("Using the full set of {} observations".format(self.lcdata.shape[0]))
            data = self.lcdata

        # Subset to get feature data
        x_df = data.loc[:, continuous_cols + categorical_cols]

        # Update our X dataframe with categorical values replaced by one-hot encoded values
        x_df = encode_categorical(x_df, categorical_cols)

        # Ensure all numeric features are on the same scale
        for col in continuous_cols:
            x_df[col] = (x_df[col] - x_df[col].mean()) / x_df[col].std()

        # Specify the target labels and flatten the array
        y = pd.get_dummies(data[label_col])

        # Create train and test sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x_df, y, test_size=test_size, random_state=23)
    
    def train_model(self, model_func, gpu_enabled=False):
        """Create and train the neural network model"""

        # Create model using provided model function
        self.model = model_func(self.x_train.shape[1], self.y_train.shape[1])

        # Model converges faster on larger data set with larger batches
        epochs = 30 if gpu_enabled else 45

        # GPU is actually *slower* than CPU when using small batch size
        batch_sz = 1024 if gpu_enabled else 64

        print("Beginning model training with batch size {} and {} epochs".format(batch_sz, epochs))

        # train the model
        return self.model.fit(self.x_train.as_matrix(),
                        self.y_train.as_matrix(),
                        validation_split=0.2,
                        epochs=epochs,  
                        batch_size=batch_sz, 
                        verbose=2)

def encode_categorical(frame, categorical_cols):
    """Replace categorical variables with one-hot encoding in-place"""
    for col in categorical_cols:
        # use get_dummies() to do one hot encoding of categorical column
        frame = frame.merge(pd.get_dummies(frame[col]), left_index=True, right_index=True)
        
        # drop the original categorical column
        frame.drop(col, axis=1, inplace=True)
  
    return frame
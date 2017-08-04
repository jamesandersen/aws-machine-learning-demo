"""
Cleanup some missing data and convert other columns for lending club data
"""
import sys
import datetime
import pandas as pd

def num_days_from_mmm_yyyy(date_str):
    """
    Convert a MMM-YYYY date string value to a numeric days value
    """
    date = datetime.datetime.strptime(date_str, '%b-%Y').date()
    delta = datetime.datetime.today().date() - date
    return delta.days

def loan_to_income(row):
    """
    Calculate a loan to income statistic
    """
    if row["application_type"] == "INDIVIDUAL":
        return row["loan_amnt"] / row["annual_inc"]
    else:
        return row["loan_amnt"] / row["annual_inc_joint"]

def il_util_ex_mort(row):
    """
    Calculate utilization on installment accounts excluding mortgage balance
    """
    if row["total_il_high_credit_limit"] > 0:
        return row["total_bal_ex_mort"] / row["total_il_high_credit_limit"]

    return 0

def installment_pct_inc(row):
    """
    Calculate the percentage of monthly income the installment payment represents
    """
    if row["application_type"] == "INDIVIDUAL":
        return row["installment"] / (row["annual_inc"] / 12)
    else:
        return row["installment"] / (row["annual_inc_joint"] / 12)

def adjusted_dti(row):
    """
    Calculate the percentage of monthly income the installment payment represents
    """
    if row["application_type"] == "INDIVIDUAL":
        return (row["loan_amnt"] + row["tot_cur_bal"]) / row["annual_inc"]
    else:
        return (row["loan_amnt"] + row["tot_cur_bal"])  / row["annual_inc_joint"]

def txt_to_pct(pct_txt):
    """
    Convert pct expressed in text e.g. "39.3 %" to float value
    """
    if isinstance(pct_txt, str):
        return float(pct_txt.replace("%", ""))

    return pct_txt

def print_null_check(dataframe, col):
    """Print number of null values in dataframe column"""
    print("{} null values in column {}".format(sum(pd.isnull(dataframe[col])), col))

def main():
    """
    Read in raw CSV and output sanitized version
    """
    print("Opening loan-stats-2015_partial.csv...")
    data = pd.read_csv("LoanStats3d_securev1.csv", low_memory=False)

    # Missing values for these columns seem most appropriate to fill with zero
    fill_zero = [
        "inq_fi",
        "inq_last_12m",
        "num_tl_120dpd_2m",
        "open_il_12m",
        "open_il_24m",
        "open_rv_12m",
        "open_rv_24m"
    ]
    for col in fill_zero:
        data[col] = data[col].fillna(0)
        print_null_check(data, col)

    # Missing values for these columns seem most appropriate to
    #  fill with the mean value for the column
    fill_mean = [
        "bc_util", # Ratio of tot current balance to high credit/credit limit for all bankcard accts
        "max_bal_bc", # Maximum current balance owed on all revolving accounts
        "open_acc_6m", # Number of open trades in last 6 months
        "open_il_6m",
        "num_rev_accts",
        "bc_open_to_buy",  # Total open to buy on revolving bankcards.
        "percent_bc_gt_75", # Percentage of all bankcard accounts > 75% of limit.
        "total_bal_il", # Total current balance of all installment accounts
        "total_il_high_credit_limit", # Total installment high credit/credit limit
        "total_cu_tl" # Number of finance trades
    ]

    for col in fill_mean:
        data[col] = data[col].fillna(data[col].mean())
        print_null_check(data, col)

    # Missing values for these columns seem most appropriate to fill with the column max
    fill_max = [
        "mo_sin_old_il_acct",
        "mths_since_last_delinq",
        "mths_since_last_major_derog",
        "mths_since_last_record",
        "mths_since_rcnt_il",
        "mths_since_recent_bc",
        "mths_since_recent_bc_dlq",
        "mths_since_recent_inq",
        "mths_since_recent_revol_delinq",
    ]

    for col in fill_max:
        data[col] = data[col].fillna(data[col].max())
        print_null_check(data, col)

    # Fill debt to income joint with individual debt to income where missing
    data["dti_joint"] = data["dti_joint"].fillna(data["dti"])
    print_null_check(data, "dti_joint")

    # Fill annual income joint with individual annual income where missing
    data["annual_inc_joint"] = data["annual_inc_joint"].fillna(data["annual_inc"])
    print_null_check(data, "annual_inc_joint")

    # Ratio of total current balance to high credit/credit limit on all install acct
    print_null_check(data, "total_bal_il")
    print_null_check(data, "total_il_high_credit_limit")
    # avoid introducing NaN via divide by zero
    data["total_il_high_credit_limit"]=data["total_il_high_credit_limit"].replace(0, data["total_il_high_credit_limit"].mean())
    data["il_util"] = data["il_util"].fillna(data["total_bal_il"] / data["total_il_high_credit_limit"] * 100)
    print_null_check(data, "il_util")

    # Revolving line utilization rate, or the amount of credit the
    # borrower is using relative to all available revolving credit.
    print_null_check(data, "revol_bal")
    print_null_check(data, "total_rev_hi_lim")
    # avoid introducing NaN via divide by zero
    data["total_rev_hi_lim"]=data["total_rev_hi_lim"].replace(0,data["total_rev_hi_lim"].mean())
    data["revol_util"] = data["revol_util"].fillna(data["revol_bal"] / data["total_rev_hi_lim"] * 100)
    print_null_check(data, "revol_util")

    # Balance to credit limit on all trades
    # avoid introducing NaN via divide by zero
    data["tot_hi_cred_lim"]=data["tot_hi_cred_lim"].replace(0,data["tot_hi_cred_lim"].mean())
    data["all_util"] = data["all_util"].fillna(data["tot_cur_bal"] / data["tot_hi_cred_lim"] * 100)
    print_null_check(data, "all_util")

    # Remove percent sign
    data['int_rate'] = data['int_rate'].map(txt_to_pct)
    print_null_check(data, "int_rate")
    print(data['int_rate'].describe())

    data['revol_util'] = data['revol_util'].map(txt_to_pct)
    print_null_check(data, "revol_util")
    print(data['revol_util'].describe())

    # Create age column
    data['age_earliest_cr'] = data['earliest_cr_line'].map(num_days_from_mmm_yyyy)
    print_null_check(data, "age_earliest_cr")
    print(data['age_earliest_cr'].describe())

    # Create loan to income, il_util_ex_mort columns
    for col, func in [
            ("loan_to_income", loan_to_income),
            ("il_util_ex_mort", il_util_ex_mort),
            ("installment_pct_inc", installment_pct_inc),
            ("adjusted_dti", adjusted_dti)]:
        data[col] = data.apply(func, axis=1)
        print_null_check(data, col)
        print(data[col].describe())

    dest = "lc-2015-loans-{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%dT%H-%M"))

    # Support optional destination supplied on command line
    if len(sys.argv) > 1:
        dest = sys.argv[1]

    data.to_csv(dest, index=False)

if __name__ == '__main__':
    main()

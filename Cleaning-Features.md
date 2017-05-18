# Data Cleaning
* Revol_util => remove “%” from text to use as numeric variable
* Replacing missing values =>
* Zeros
* Mean
* Max
* custom

# Feature Engineering
* Earliest_cr_line => Convert from categorical to continuous “age” variable in days 
* Loan_to_income => Loan as percentage of annual income (adjusted for application type)
* Il_util_ex_mort => Calculate utilization on installment accounts excluding mortgage balance
* Installment_pct_inc =>  projected loan payment as a percentage of annual income adjusted for application type
* Adjusted_dti => What will DTI look like if the loan is issued, adjusted for application type

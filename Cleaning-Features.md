# Data Cleaning
In our loan data set, several variables have missing values or are not formatted so that we can use them properly.  For example:

* Missing Values
    * “number of personal finance inquiries” (`inq_fi`)
    * “months since borrower’s last delinquency” (`mths_since_last_delinq`)
    * "Percentage of all bankcard accounts > 75% of limit." (`percent_bc_gt_75`) 
* Formatting Issues
    * "Interest Rate" (`int_rate`) - Contains a "%" character preventing it from being used as a numeric variable

Replacing missing values with the mean of existing values or zero are common practices but these decisions should really be driven by knowledge of the data and business domain.  For this open dataset I’ve made some judgement calls about when to replace with zero, the mean or the max value:
* “number of personal finance inquiries” - I'm assuming a missing value here means there are no personal finance inquiries so a zero is appropriate
*  "“months since borrower’s last delinquency”" - Here I assume that a missing value indicates there has been no delinquency and this is a continuous/numeric variable rather than categorical so the most appropriate value is (other than infinity which would break the calculations) feels like the max value in the dataset
* "Percentage of all bankcard accounts > 75% of limit" - Zero might be a valid assumption here but in this case I'll assume that every applicant is somewhere on the spectrum and use the mean value for the data


# Feature Engineering
A close look at the data can also give us some ideas on additional features that might be useful in our predictive model a.k.a “feature engineering”.  For example:
* **Age of Earliest Credit Line** - `earliest_cr_line` is a date variable in the format `MMM-YYYY` but it might be more useful to present the **number of days** since a credit line was first opened by transforming that value to an numeric count of days since the date
* **Loan to Income** - While we have both the loan amount and borrowers income in the data we don't have a ratio presenting the loan amount as a percentage of annual income

See [lending_club_clean.py](lending_club_clean.py) for details on all the cleaning and feature engineering performed on the raw dataset.

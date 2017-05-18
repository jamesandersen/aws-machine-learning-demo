# AWS Maching Learning Walkthrough
This is a simple walkthrough intended to introduce [Amazon's Machine Learning service](http://docs.aws.amazon.com/machine-learning/latest/dg/what-is-amazon-machine-learning.html) in the context trying to predict loan interest rates and grades.

We’re going to use some [publicly available loan applicant data](https://www.lendingclub.com/info/download-data.action) from Lending Club.  The data set I’ve chosen contains over 420,000 loans with data such as applicant annual income, loan term, state of residence, credit score range and a number of other credit data, etc.  The dataset also contains a letter grade classification of the loan in the range A - G.  We’re going to use AWS machine learning to build two models, one that will predict an appropriate interest rate and a second that will infer the letter grade for the loan application.

1. [Creating a Datasource](Create-Datasource.md)
2. [Data Cleaning and Feature Engineering](Cleaning-Features.md)
3. [Creating the Machine Learning Model](Model-Creation.md)
4. [Gotchas and Limitations](Gotchas-Limitations.md)






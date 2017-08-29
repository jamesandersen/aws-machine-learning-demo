#!/bin/bash -xe

# UPDATE THESE AS NECESSARY
aws_cli_profile=um
s3_bucket=um-aws-machine-learning-demo
region=us-west-1

# Build the lambda deploy package using previously created runtime zip (see build-lambda-pkg.sh)
cp keras-tf-runtime.zip lamda-lc-predict-pkg.zip

# Copy our handler code into our deployment package
zip lamda-lc-predict-pkg.zip handler.py

#: <<'END'
aws s3 cp lamda-lc-predict-pkg.zip s3://$s3_bucket/ --storage-class REDUCED_REDUNDANCY --profile $aws_cli_profile
rm lamda-lc-predict-pkg.zip

aws cloudformation  create-stack \
    --template-body file://lambda.template \
    --stack-name lambda-lc-predictions \
    --parameters ParameterKey=ModelBucket,ParameterValue=$s3_bucket \
        ParameterKey=ModelKey,ParameterValue=2017-08-28T19_52/lc_model.h5 \
        ParameterKey=PackageKey,ParameterValue=lamda-lc-predict-pkg.zip \
    --capabilities CAPABILITY_IAM \
    --profile $aws_cli_profile --region $region

# Wait for the stack to be created
aws cloudformation wait stack-create-complete --stack-name lambda-lc-predictions --profile $aws_cli_profile --region $region
#END

# Finally, test with CURL
api_url=`aws cloudformation list-exports --profile $aws_cli_profile --region $region --query "Exports[?Name == 'LoanPredictAPIUrl'].Value"`
curl -H "Content-Type: application/json" --data @test.json ${api_url}/predict/loan-grade
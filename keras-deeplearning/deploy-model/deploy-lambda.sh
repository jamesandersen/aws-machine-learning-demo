#!/bin/bash -xe

rm -rdf pkg/

mkdir pkg/

unzip keras-tf-runtime.zip -d pkg/

cp handler.py pkg/

aws cloudformation deploy \
    --template-file lambda.template \
    --stack-name lambda-lc-predictions \
    --capabilities CAPABILITY_IAM \
    --profile um --region us-west-1

# Test with:
api_url=`aws cloudformation list-exports --profile um --region us-west-1 --query "Exports[?Name == 'LoanPredictAPIUrl'].Value"`
curl -H "Content-Type: application/json" --data @test.json ${api_url}/predict/loan-grade
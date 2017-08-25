#!/bin/bash -xe

rm -rdf pkg/

mkdir pkg/

#unzip keras-tf-py36-pkg.zip -d pkg/
unzip keras-tf-runtime.zip -d pkg/

cp handler.py pkg/

#rm -rdf pkg
#: <<'END'
aws cloudformation package \
    --template-file lambda.template \
    --s3-bucket um-aws-machine-learning-demo \
    --output-template-file packaged-lambda.template \
    --profile um --region us-west-1

aws cloudformation deploy \
    --template-file packaged-lambda.template \
    --stack-name lambda-lending-club-predictions \
    --capabilities CAPABILITY_IAM \
    --profile um --region us-west-1
#END

# Test with:
# curl -H "Content-Type: application/json" --data @test.json https://<your-api-gateway-id>.execute-api.us-west-1.amazonaws.com/Stage/predict/loan-grade
#!/bin/bash -xe

aws cloudformation validate-template --template-body file://train-model.template

#: <<'END'
aws cloudformation create-stack --stack-name deep-learning-spot-instance --template-body file://train-model.template \
    --parameters ParameterKey=InstanceType,ParameterValue=p2.xlarge \
        ParameterKey=SpotBidPrice,ParameterValue=0.75 \
        ParameterKey=KeyPairName,ParameterValue=UMOregon \
        ParameterKey=GitRepo,ParameterValue=https://github.com/jamesandersen/aws-machine-learning-demo.git \
        ParameterKey=GitBranch,ParameterValue=aws-keras-deeplearning \
        ParameterKey=RunScript,ParameterValue=keras-deeplearning/train_model.sh \
    --capabilities CAPABILITY_NAMED_IAM \
    --disable-rollback \
    --region us-west-2 \
    --profile um
#END
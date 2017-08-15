#!/bin/bash -xe

aws cloudformation validate-template --template-body file://train-model.template

#: <<'END'
aws cloudformation create-stack --stack-name deep-learning-spot --template-body file://train-model.template \
    --parameters ParameterKey=InstanceType,ParameterValue=p2.xlarge \
        ParameterKey=SpotBidPrice,ParameterValue=0.50 \
        ParameterKey=KeyPairName,ParameterValue=UMOregon \
        ParameterKey=SourceCidr,ParameterValue=96.60.192.215/32 \
        ParameterKey=GitRepo,ParameterValue=https://github.com/jamesandersen/aws-machine-learning-demo.git \
        ParameterKey=GitBranch,ParameterValue=aws-keras-deeplearning \
        ParameterKey=RunScript,ParameterValue=keras-deeplearning/train-model/train_model.sh \
        ParameterKey=OutputBucket,ParameterValue=um-aws-machine-learning-demo \
    --capabilities CAPABILITY_NAMED_IAM \
    --disable-rollback \
    --region us-west-2 \
    --profile um
#END
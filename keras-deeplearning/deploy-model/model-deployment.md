# Deploying a Machine Learning Model with AWS Lambda

After training our model (see [`model-creation.md`](../model-creation.md)) we should have a saved Keras model (*.h5) available in an S3 bucket.  Now we need a way to use the model to make loan grade predictions on the fly as we see new loan data.  [AWS Lambda](https://aws.amazon.com/lambda/) is a scalable compute option that can be triggered by a wide variety of events in an AWS infrastructure.   While the Keras model can be used in several ways, we focus here on using it from an AWS Lambda function.

The biggest hurdle with using Lambda turns out to be the 50MB limit on the deployment package that backs a Lambda function.  As the default Keras + Tensorflow installation is over 500MB, we end up needing to strip out as much as possible so that we can still come in under the 50MB (compressed) limit. [`build-lambda-pkg.sh`](build-lambda-pkg.sh) scripts the steps to do this and is intended to run using the [lambci/lambda](https://hub.docker.com/r/lambci/lambda/) docker container which simulates the Lambda environment.

From the `keras-deeplearning/deploy-model/` directory, run the following to build a Keras + TensorFlow Lambda runtime package
```
docker run -it -v `pwd`:/tmp/deploy/ lambci/lambda:build-python3.6 bash /tmp/deploy/build-lambda-pkg.sh
```
This should produce a `keras-tf-runtime.zip` file in the directory.

The final addition to our Lambda deployment package is [a handler function](handler.py) for the event that triggers the Lambda.  Its job is to load our saved model from S3, extract prediction data from the event source and make predictions. Note that loading the model introducing network and CPU latency so we do it **once** as the Lambda "warms up" then subsequent invocations of the same Lambda instance will return in ~100ms.

We can test out the Lambda locally, again using the [lambci/lambda](https://hub.docker.com/r/lambci/lambda/) docker image.   Extract the zipped deployment package to a `pkg` directory and then run:
```
docker run -v `pwd`/pkg:/var/task \
    -e "bucket=<S3 BUCKET WHERE YOU MODEL RESIDES>" \
    -e "modelkey=<KEY WHERE YOUR MODEL RESIDES>" \
    -e "AWS_ACCESS_KEY_ID=<YOUR_KEY_ID>" \
    -e "AWS_SECRET_ACCESS_KEY=<YOUR_ACCESS_KEY>" \
    lambci/lambda:python3.6 handler.sample_predict "`cat test-request.json`"

```

After a local test, we can deploy our Lambda function to AWS and wire up an API Gateway trigger.  The [`deploy-lambda.sh`](deploy-lambda.sh) script automates:
# The creation of a deployment package
# Uploading the package to S3
# Creating a Lambda function and an API gateway to trigger it
    * See (lambda.template) for details
# Making an HTTP request to the API gateway with `curl`
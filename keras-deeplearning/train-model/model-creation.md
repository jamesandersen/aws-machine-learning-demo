# Building and Creating a Model

## Working Locally
A first step in building up a machine learning pipeline is getting familiar with our data.  Checkout [the Jupyter notebook](lending-club-loan-grades.ipynb) to see how data is loaded, explored with some visualizations and prepped for machine learning.  The [the Jupyter notebook](lending-club-loan-grades.ipynb) continues on with the creation of a fairly simply neural network using [Keras](https://keras.io/) and then trains the model using a subset of the data.   We want to see if our model passes a "smell test" before training it on the full dataset using high-powered GPU machines.

You can run keras and jupyter locally using a docker image and a volume mapped to the working directory of the repo.  From the `/keras-deeplearning/train-model/` directory, run:
```
docker run -d -p 8888:8888 -v `pwd`/:/srv -e "sample=50000" gw000/keras-full:latest
```

## Training the model
Once we feel like we have a suitable model structure that is behaving well on our subset of data, we'll want to train it using the full dataset and high-powered machines.   The [`train-model.template`](train-model.template) is a CloudFormation template that will launch a spot instance of one of the AWS GPU instance types using the [AWS Deep Learning AMI](https://aws.amazon.com/amazon-ai/amis/).  The template takes in several parameters and can be easily launched using (deploy-stack.sh).  It does the following:
* Builds up a custom VPC to which the spot instance will be deployed
* Launches a GPU instance (the specific instance type is a parameter)
   * The GPU instance will be running using a role that grants access to an S3 bucket from which data may be loaded and to which outputs can be saved
* Checks out a Git repo on the instance (passed via parameter)
* Runs a script **from the git repo** on the instance which should kick off the training
   * The script should save any outputs, including the trained model, to the S3 bucket for persistence

Review [`train-model.template`](train-model.template) for full details.

We end up with a much more accurate model relative to that created with the AWS Machine Learning service.
![Confusion Matrix Comparison](images/neural_net_confusion_matrix.png)
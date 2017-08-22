
Run keras and jupyter via docker and data and notebook directories:
```
docker run -d -p 8888:8888 -v `pwd`/:/srv -e "sample=50000" gw000/keras-full:latest
```

Run an image to build lambda deploy package
```
docker run -it -v `pwd`:/tmp/deploy/ lambci/lambda:build-python3.6 bash /tmp/deploy/build-lambda-pkg.sh
```

Test out the deployment package locally

```
docker run -v `pwd`/pkg:/var/task \
     -e "bucket=um-aws-machine-learning-demo" \
     -e "modelkey=2017-08-18T20_33/lc_model.h5" \
     lambci/lambda:python3.6 \
     handler.sample_predict \
     "`cat test.json`"

```
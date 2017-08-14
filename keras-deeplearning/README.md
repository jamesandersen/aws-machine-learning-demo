
Run keras and jupyter via docker and data and notebook directories:
```
docker run -d -p=6006:6006 -p 8888:8888 \
    -v `pwd`/:/srv \
    -e "sample=50000" \
    gw000/keras-full:latest
                
```

Run an image to build lambda deploy package
```
docker run -it -v `pwd`/lambda-deploy:/home/lambda-deploy lambci/lambda:build-python3.6 bash
                
```

References:
* https://www.datacamp.com/community/tutorials/deep-learning-python#gs.j5r4HVU
* http://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
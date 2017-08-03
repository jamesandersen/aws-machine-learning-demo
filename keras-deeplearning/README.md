Build docker image that simulates the AWS Deep Learning AMI:
```
docker build -t jander/keras-full:local .
```


Run keras and jupyter via docker and data and notebook directories:
```
docker run -d -p=6006:6006 -p 8888:8888 \
    -v `pwd`/:/srv \
    -e "sample=50000" \
    jander/keras-full:local
                
```

References:
* https://www.datacamp.com/community/tutorials/deep-learning-python#gs.j5r4HVU
* http://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
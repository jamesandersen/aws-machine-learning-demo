
Run keras and jupyter via docker and data and notebook directories:
```
docker run -d -p=6006:6006 -p 8888:8888 \
    -v `pwd`/:/srv \
    -e "sample=50000" \
    gw000/keras-full:1.2.0
                
```

References:
* https://www.datacamp.com/community/tutorials/deep-learning-python#gs.j5r4HVU
* http://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
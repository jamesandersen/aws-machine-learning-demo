Run keras and jupyter via docker and data and notebook directories:
```
docker run -d -p=6006:6006 -p 8888:8888 -v `pwd`/:/srv -v `pwd`/../data/:/tmp/lcdata gw000/keras-full:latest
                
```
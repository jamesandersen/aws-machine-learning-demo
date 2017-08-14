#!/bin/bash -xe

python -m venv ~/keras-tf
source ~/keras-tf/bin/activate
pip install tensorflow keras

site_pkgs=$VIRTUAL_ENV/lib/python3.6/site-packages/

# check entire directory size
du -sh $site_pkgs
find $site_pkgs -name "*.so" | xargs strip
du -sh $site_pkgs

# Remove tests
find $site_pkgs -wholename "*/tests/*" -exec rm -rdf {} +
find $site_pkgs -name "unittest*" -exec rm {} +

# Remove info directories
find $site_pkgs -name "*-info" -type d -exec rm -rdf {} +

# This is duplicated in numpy/.libs  ...and it's huge!
rm $site_pkgs/scipy/.libs/libopenblasp-r0-39a31c03.2.18.so
rm $site_pkgs/scipy/.libs/libgfortran-ed201abd.so.3.0.0


rm $site_pkgs/scipy/misc/face.dat

rm $site_pkgs/keras/backend/theano_backend.py
rm $site_pkgs/keras/backend/cntk_backend.py

rm -rdf $site_pkgs/external/
rm -rdf $site_pkgs/tensorflow/include/external/eigen_archive/

# Remove .js
find $site_pkgs -name "*.js" -exec rm -rdf {} +
find $site_pkgs -name "*.html" -exec rm -rdf {} +

rm -rdf $site_pkgs/theano/
rm -rdf $site_pkgs/pip/
rm -rdf $site_pkgs/setuptools/
rm -rdf $site_pkgs/bleach/

python -c 'import keras'

# Remove cached files
find $site_pkgs -wholename "*/__pycache__" -exec rm -rdf {} +

#zip -r ~/tf_env.zip . --exclude \*.pyc --exclude \*.html --exclude \*.js
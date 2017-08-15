#!/bin/bash -xe

python -m venv ~/keras-tf
source ~/keras-tf/bin/activate
pip install tensorflow keras

site_pkgs=$VIRTUAL_ENV/lib/python3.6/site-packages

# check entire directory size
du -sh $site_pkgs
find $site_pkgs -name "*.so" | xargs strip

# Remove tests
find $site_pkgs -wholename "*/tests/*" -exec rm -rdf {} +
find $site_pkgs -name "unittest*" -exec rm {} +

# Should come after the strip *.so command
# and removal of tests above to avoid errors
pip install h5py

# Remove info directories
find $site_pkgs -name "*-info" -type d -exec rm -rdf {} +

# Remove *.html / *.js
find $site_pkgs -name "*.js" -exec rm -rdf {} +
find $site_pkgs -name "*.html" -exec rm -rdf {} +

# Remove *.h files, for runtime only; we won't be linking via header files
find $site_pkgs -name "*.h" -exec rm -rdf {} +

# Remove python environment tools not needed at runtime
rm -rdf $site_pkgs/pip/
rm -rdf $site_pkgs/setuptools/
rm -rdf $site_pkgs/wheel/

# Remove unused TensorFlow dependencies
rm -rdf $site_pkgs/external/
rm -rdf $site_pkgs/tensorflow/include/external/eigen_archive/
rm -rdf $site_pkgs/bleach/
rm -rdf $site_pkgs/html5lib/
rm -rdf $site_pkgs/markdown/

# Remove Theano and related files/deps
rm -rdf $site_pkgs/theano/
rm -rdf $site_pkgs/scipy/ # Theano dependency
# These large files are duplicated in numpy/.libs
# rm $site_pkgs/scipy/.libs/libopenblasp-r0-39a31c03.2.18.so
# rm $site_pkgs/scipy/.libs/libgfortran-ed201abd.so.3.0.0
# rm $site_pkgs/scipy/misc/face.dat
rm -rdf $site_pkgs/bin/ # Theano related scripts

# Remove unused Keras backends
rm $site_pkgs/keras/backend/theano_backend.py
rm $site_pkgs/keras/backend/cntk_backend.py

python -c 'import keras'

# Remove cached files
find $site_pkgs -wholename "*/__pycache__" -exec rm -rdf {} +

du -sh $site_pkgs
cd $site_pkgs
echo "Zipping up python 3.6 deployment package"
zip -r -9 /tmp/deploy/keras-tf-py36-pkg.zip .
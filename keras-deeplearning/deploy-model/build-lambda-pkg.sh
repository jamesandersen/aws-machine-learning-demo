#!/bin/bash -xe

python -m venv ~/keras-tf
source ~/keras-tf/bin/activate
pip install tensorflow 'keras==2.0.6'

site_pkgs=$VIRTUAL_ENV/lib/python3.6/site-packages

# check entire directory size
du -sh $site_pkgs

# strip C libraries
find $site_pkgs -name "*.so" | xargs strip

# Remove tests
find $site_pkgs -wholename "*/tests/*" -exec rm -rdf {} +
find $site_pkgs -name "unittest*" -exec rm {} +

# Should come after the strip *.so command
# and removal of tests above to avoid errors - these C libs are not "strippable"
pip install h5py

# Remove info directories
find $site_pkgs -name "*-info" -type d -exec rm -rdf {} +

# Remove *.html / *.js
find $site_pkgs -name "*.js" -exec rm -rdf {} +
find $site_pkgs -name "*.html" -exec rm -rdf {} +

# Remove *.h files; for runtime we won't be linking via header files
find $site_pkgs -name "*.h" -exec rm -rdf {} +

# Remove python environment tools not needed at runtime
rm -rdf $site_pkgs/pip/
rm -rdf $site_pkgs/setuptools/
rm -rdf $site_pkgs/wheel/
rm -rdf $site_pkgs/pkg_resources/
rm $site_pkgs/easy_install.py


# Remove unused TensorFlow dependencies
rm -rdf $site_pkgs/external/
rm -rdf $site_pkgs/tensorflow/include/external/eigen_archive/
rm -rdf $site_pkgs/tensorflow/include/Eigen/src/
rm $site_pkgs/protobuf-3.4.0-py3.6-nspkg.pth

rm -rdf $site_pkgs/tensorflow/debug/
rm -rdf $site_pkgs/tensorflow/examples/
rm -rdf $site_pkgs/tensorflow/include/
rm -rdf $site_pkgs/tensorflow/python/debug/
rm -rdf $site_pkgs/tensorflow/python/tools/
rm -rdf $site_pkgs/tensorflow/tools/
rm -rdf $site_pkgs/numpy/distutils/
rm -rdf $site_pkgs/numpy/doc/
rm -rdf $site_pkgs/werkzeug/
rm -rdf $site_pkgs/bleach/
rm -rdf $site_pkgs/html5lib/
rm -rdf $site_pkgs/markdown/

# Remove Theano and related files/deps
rm -rdf $site_pkgs/theano/
rm -rdf $site_pkgs/tensorboard/
rm -rdf $site_pkgs/scipy/ # Theano dependency
rm -rdf $site_pkgs/bin/ # Theano related scripts

# Remove unused Keras backends
rm $site_pkgs/keras/backend/theano_backend.py
rm $site_pkgs/keras/backend/cntk_backend.py

# Test keras
python -c 'import keras'

## declare an array variable
declare -a arr=("keras" "numpy" "yaml"  "google" "h5py")

## now loop through the above array
for mod in "${arr[@]}"
do
   # Leave module precompiles for faster Lambda startup
    find $site_pkgs/$mod -name '*.pyc' | while read line; do
        dest="${line//.cpython-36/}"
        dest="${dest//\/__pycache__}"
        mv $line $dest
    done

    # Remove the module's source files
    find $site_pkgs/$mod -name "*.py" -exec rm {} +
done

# Remove cached files
#find $site_pkgs -wholename "*/google/*/__pycache__" -exec rm -rdf {} +
#find $site_pkgs -wholename "*/h5py/*/__pycache__" -exec rm -rdf {} +

du -sh $site_pkgs
cd $site_pkgs
echo "Zipping up python 3.6 deployment package"
zip -r -9 /tmp/deploy/keras-tf-runtime.zip .
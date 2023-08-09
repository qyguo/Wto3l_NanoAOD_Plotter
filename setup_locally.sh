export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/python3/3.8.2/lib:$LD_LIBRARY_PATH
export PATH="/cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/python3/3.8.2/bin:$PATH"

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install uproot3_methods
python3 -m pip install uproot
#python3 -m pip install numpy
python3 -m pip install matplotlib
python3 -m pip install pickle
python3 -m pip install tqdm
python3 -m pip install prettytable
## install all the needed package by the same command
## If u need to install it to the certain PATH, take the --prefix or --target such as,
## python3 -m pip install scipy --prefix /workfs2/cms/qyguo/.local/ #(consider the dependence)
## python3 -m pip install scipy --target /workfs2/cms/qyguo/.local/
## Check whether it is installed and version by the following command:
## python3 -c "import sys; sys.path.append('/workfs2/cms/qyguo/.local/lib/python3.8/site-packages'); import scipy; print(scipy.__version__)"
## By the way, i use the uproot3_methods instead of uproot_methods to avoid the conflict between the numpy used by uproot so do not forget alter the code. 
## When running the code, u may meet some certain issue by this locally-running method and then we need to do some corresponding modification. 


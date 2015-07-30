#!/bin/bash

# make and activate environment
virtualenv --always-copy environment
. environment/bin/activate


cd environment
mkdir build
cd build

# install requirements
pip install -r ../../requirements.txt

# download and install sip
wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.15.4/sip-4.15.4.zip
unzip sip-4.15.4.zip
cd sip-4.15.4
python configure.py --incdir=../environment/include/python2.7
make
make install
cd ..

rm -r sip*

# download and install PyQt
# ATTENTION: this may take a while
wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.3/PyQt-x11-gpl-4.10.3.tar.gz
tar zxvf PyQt-x11-gpl-4.10.3.tar.gz
cd PyQt-x11-gpl-4.10.3
python configure.py
make
make install

rm -r PyQt*



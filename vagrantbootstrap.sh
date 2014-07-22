#!/usr/bin/env bash
apt-get update
apt-get -y install python3.2
apt-get -y install python3.2-dev
apt-get -y install python3-setuptools
apt-get -y install python3-tk
apt-get -y install swig
apt-get -y install python3-twisted
apt-get -y install g++
easy_install3 distribute
easy_install3 pip
easy_install3 twisted
pip3 install twisted
easy_install3 Box2D
pip3 install Box2D
easy_install3 Pillow
pip3 install Pillow
easy_install3 cx_Freeze
pip3 install cx_Freeze
apt-get -y install mercurial python3-numpy ffmpeg libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
python3 setup.py install
cd ..
rm -rf pygame
apt-get -y install xinit lxde
startx

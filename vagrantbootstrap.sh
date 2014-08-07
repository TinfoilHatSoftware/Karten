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
export DEBIAN_FRONTEND=noninteractive

sudo apt-get update

# ---- OSS AUDIO
sudo usermod -a -G audio vagrant
sudo apt-get install -y oss4-base oss4-dkms oss4-source oss4-gtk linux-headers-3.2.0-23 debconf-utils
sudo ln -s /usr/src/linux-headers-$(uname -r)/ /lib/modules/$(uname -r)/source || echo ALREADY SYMLINKED
sudo module-assistant prepare
sudo module-assistant auto-install -i oss4 # this can take 2 minutes
sudo debconf-set-selections <<< "linux-sound-base linux-sound-base/sound_system select  OSS"
echo READY.

# have to reboot for drivers to kick in, but only the first time of course
if [ ! -f ~/runonce ]
then
  sudo reboot
  touch ~/runonce
fi
startx

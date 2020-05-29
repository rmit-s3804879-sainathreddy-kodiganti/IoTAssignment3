--- Installing OpenCV on Pi ---

https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/

Note the installation could take some time to complete (for me ~1 hour).

sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove

sudo apt-get update && sudo apt-get upgrade

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev
sudo apt-get install libcanberra-gtk*
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install python2.7-dev python3-dev

cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib.zip

pip3 install numpy

cd ~/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

# Update CONF_SWAPSIZE to a larger size.
sudo nano /etc/dphys-swapfile

# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
# CONF_SWAPSIZE=100
CONF_SWAPSIZE=1024

sudo /etc/init.d/dphys-swapfile restart

make -j4

sudo make install
sudo ldconfig

# Reset CONF_SWAPSIZE to a smaller size.
sudo nano /etc/dphys-swapfile

# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
CONF_SWAPSIZE=100
# CONF_SWAPSIZE=1024

sudo /etc/init.d/dphys-swapfile restart

cd /usr/local/lib/python3.5/dist-packages/

sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

cd ~

# Test OpenCV.
python3

>>> import cv2
>>> cv2.__version__
'3.3.0'
>>> quit()

--- Installing dlib and face_recognition python3 packages ---

Note the installation could take some time to complete (for me about more than 2 hours).

https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

sudo apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip

sudo apt-get install python3-picamera

pip3 install --upgrade picamera[array]

# Update CONF_SWAPSIZE to a larger size.
sudo nano /etc/dphys-swapfile

# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
# CONF_SWAPSIZE=100
CONF_SWAPSIZE=1024

sudo /etc/init.d/dphys-swapfile restart

pip3 install dlib
pip3 install face_recognition

# Reset CONF_SWAPSIZE to a smaller size.
sudo nano /etc/dphys-swapfile

# set size to absolute value, leaving empty (default) then uses computed value
#   you most likely don't want this, unless you have an special disk situation
CONF_SWAPSIZE=100
# CONF_SWAPSIZE=1024

sudo /etc/init.d/dphys-swapfile restart

--- Installing imutils python3 package ---

pip3 install imutils

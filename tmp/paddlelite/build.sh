# 更新库
sudo apt update
sudo apt install -y vim git wget unzip build-essential openjdk-8-jre default-jdk adb

# 下载ndk-r17c
export NDK=android-ndk-r17c
cd /tmp
sudo wget -c https://dl.google.com/android/repository/${NDK}-linux-x86_64.zip
cd /opt
sudo unzip /tmp/${NDK}-linux-x86_64.zip
echo "export NDK_ROOT=/opt/${NDK}" >> ~/.bashrc
echo "export ANDROID_NDK=${NDK_ROOT}" >> ~/.bashrc

# 下载cmake 3.11.0-rc4
cd /tmp
wget -c https://cmake.org/files/v3.11/cmake-3.11.0-rc4-Linux-x86_64.tar.gz
sudo tar zxvf cmake-3.11.0-rc4-Linux-x86_64.tar.gz
sudo mv cmake-3.11.0-rc4-Linux-x86_64  /opt/cmake-3.11
sudo ln -sf /opt/cmake-3.11/bin/*  /usr/bin/

# 编译paddlelite
mkdir ~/code
cd ~/code
git clone https://github.com/PaddlePaddle/Paddle-Lite.git
cd Paddle-Lite
./lite/tools/build.sh --arm_os=android \
  --arm_abi=armv8 \
  --arm_lang=gcc \
  --android_stl=c++_static \
  full_publish
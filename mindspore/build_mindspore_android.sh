
wget -c https://dl.google.com/android/repository/android-ndk-r21b-linux-x86_64.zip
unzip -q android-ndk-r21b-linux-x86_64.zip
export ANDROID_NDK_HOME=$(pwd)/android-ndk-r21b-linux-x86_64
wget -c https://github.com/Kitware/CMake/releases/download/v3.18.2/cmake-3.18.2-Linux-x86_64.tar.gz
tar -zxvfq cmake-3.18.2-Linux-x86_64.tar.gz

export CMAKE_HOME=$(pwd)/cmake-3.18.2-Linux-x86_64
echo $CMAKE_HOME
export PATH=${PATH}:${CMAKE_HOME}/bin/
#export PATH=${PATH}:${LLVM_ROOT}/bin:${CMAKE_ROOT}/bin

git clone https://gitee.com/mindspore/mindspore.git mindspore
cd mindspore
./build.sh -I arm32 -e gpu -j30
./build.sh -I arm64 -e gpu -j30

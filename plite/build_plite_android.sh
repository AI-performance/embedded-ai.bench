set -x

# cmake
if [ ! -f "/opt/cmake-3.10/bin/cmake"]; then
    wget -c https://mms-res.cdn.bcebos.com/cmake-3.10.3-Linux-x86_64.tar.gz && \
        tar xzf cmake-3.10.3-Linux-x86_64.tar.gz && \
        mv cmake-3.10.3-Linux-x86_64 /opt/cmake-3.10 && \  
        ln -s /opt/cmake-3.10/bin/cmake /usr/bin/cmake && \
        ln -s /opt/cmake-3.10/bin/ccmake /usr/bin/ccmake
else
    echo "local cmake existed"
fi


# download Android NDK for linux-x86_64
#    note: Skip this step if NDK installed
#    ref: https://developer.android.com/ndk/downloads
readonly ANDROID_NDK_HOME=/opt/android-ndk-r17c
if [ ! -d ${ANDROID_NDK_HOME} ]; then
    cd /tmp && wget -c https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip
    cd /opt && unzip /tmp/android-ndk-r17c-linux-x86_64.zip
    cd -
else
    echo "local ${ANDROID_NDK_HOME} existed"
fi
export ANDROID_NDK=${ANDROID_NDK_HOME}
export NDK_ROOT=${ANDROID_NDK_HOME}

git clone https://github.com/PaddlePaddle/Paddle-Lite.git plite
cd plite


# build android armv7
./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv7 \
 --arm_lang=clang \
 --android_stl=c++_static \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

# build android armv8
./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv8 \
 --arm_lang=clang \
 --android_stl=c++_static \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

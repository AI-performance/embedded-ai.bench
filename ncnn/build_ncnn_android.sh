#!/bin/bash
set -x

readonly ANDROID_NDK_HOME=/opt/android-ndk-r17c

function prepare_env {
    # attr, wget, unzip
    apt update
    apt install -y --no-install-recommends attr wget unzip

    # cmake
    if [ ! -f "/opt/cmake-3.10/bin/cmake" ]; then
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
    if [ ! -d ${ANDROID_NDK_HOME} ]; then
        cd /tmp && wget -c https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip
        cd /opt && unzip /tmp/android-ndk-r17c-linux-x86_64.zip
    else
	echo "local ${ANDROID_NDK_HOME} existed"
    fi
    export ANDROID_NDK=${ANDROID_NDK_HOME}

    cd -
}

# download code repo from github
function download_repo {
    # download repo
    if [ ! -d "./ncnn" ]; then
        git clone https://github.com/tencent/ncnn.git ncnn
    else
        echo "local ncnn repo exited"
    fi
}

# compile tnn
function build {
    cd ncnn

    # generate
    cd schema && ./generate.sh
    cd -

    # build
    export ANDROID_NDK=${ANDROID_NDK_HOME}
    cd ncnn

    ##### android armv7
    mkdir -p build-android-armv7
    pushd build-android-armv7
    cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI="armeabi-v7a" -DANDROID_ARM_NEON=ON -DANDROID_PLATFORM=android-19 ..
    make -j4
    make install
    popd

    ##### android aarch64
    mkdir -p build-android-aarch64
    pushd build-android-aarch64
    cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI="arm64-v8a" -DANDROID_PLATFORM=android-21 ..
    make -j4
    make install
    popd

    ##### android armv7 vulkan
#    mkdir -p build-android-armv7-vulkan
#    pushd build-android-armv7-vulkan
#    cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI="armeabi-v7a" -DANDROID_ARM_NEON=ON -DANDROID_PLATFORM=android-24 -DNCNN_VULKAN=ON ..
#    make -j4
#    make install
#    popd

    ##### android aarch64 vulkan
#    mkdir -p build-android-aarch64-vulkan
#    pushd build-android-aarch64-vulkan
#    cmake -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake -DANDROID_ABI="arm64-v8a" -DANDROID_PLATFORM=android-24 -DNCNN_VULKAN=ON ..
#    make -j4
#    make install
#    popd

}

function main {
    prepare_env
    download_repo
    build
}

main ${@}

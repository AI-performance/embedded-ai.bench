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
    if [ ! -d "./mnn" ]; then
        git clone https://github.com/alibaba/mnn.git mnn
    else
        echo "local mnn repo exited"
    fi
}

# shellcheck disable=SC2120
function build {
    cp MNNV2Basic.cpp ./mnn/tools/cpp/MNNV2Basic.cpp
    cp benchmark.cpp ./mnn/benchmark/benchmark.cpp
    cd mnn

    # generate
    cd schema && ./generate.sh
    cd -

    export ANDROID_NDK=${ANDROID_NDK_HOME}
    cd ./benchmark

    # build 32
    mkdir build_32
    cd build_32
    cmake ../../ \
          -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
          -DCMAKE_BUILD_TYPE=Release \
          -DANDROID_ABI="armeabi-v7a" \
          -DANDROID_STL=c++_static \
          -DCMAKE_BUILD_TYPE=Release \
          -DANDROID_NATIVE_API_LEVEL=android-21  \
          -DANDROID_TOOLCHAIN=clang \
          -DMNN_VULKAN=true \
          -DMNN_OPENCL=true \
          -DMNN_OPENMP=true \
          -DMNN_OPENGL=true \
          -DMNN_DEBUG=false \
          -DMNN_BUILD_BENCHMARK=true \
          -DMNN_BUILD_FOR_ANDROID_COMMAND=true \
          -DNATIVE_LIBRARY_OUTPUT=.
    make -j8 benchmark.out timeProfile.out

    cd -
    mkdir build_64
    cd build_64
    # build 64
    cmake ../../ \
          -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
          -DCMAKE_BUILD_TYPE=Release \
          -DANDROID_ABI="arm64-v8a" \
          -DANDROID_STL=c++_static \
          -DCMAKE_BUILD_TYPE=Release \
          -DANDROID_NATIVE_API_LEVEL=android-21  \
          -DANDROID_TOOLCHAIN=clang \
          -DMNN_VULKAN=true \
          -DMNN_OPENCL=true \
          -DMNN_OPENMP=true \
          -DMNN_OPENGL=true \
          -DMNN_DEBUG=false \
          -DMNN_BUILD_BENCHMARK=true \
          -DMNN_BUILD_FOR_ANDROID_COMMAND=true \
          -DNATIVE_LIBRARY_OUTPUT=.
    make -j8 benchmark.out timeProfile.out
}

function main {
    prepare_env
    download_repo
    build
}

main ${@}

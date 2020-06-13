#!/bin/bash
set -x

function prepare_env {
    # attr, wget, unzip
    apt update
    apt install -y --no-install-recommends attr wget unzip

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
    else
	echo "local ${ANDROID_NDK_HOME} existed"
    fi
    export ANDROID_NDK=${ANDROID_NDK_HOME}

    cd -
}

# download code repo from github
function download_repo {
    # download repo
    if [ ! -d "./tnn" ]; then
        git clone https://github.com/tencent/tnn.git tnn
    else
        echo "local tnn repo exited"
    fi
}

# compile tnn
function build {
   cd tnn/scripts/
   ./build_android.sh
}

function main {
    prepare_env
    download_repo
    build
}

main ${@}

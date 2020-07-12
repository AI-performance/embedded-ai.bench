#!/usr/bin/env bash
set -ex

function get_platform() {
    uname_a_str=`uname -a`
    if [[ $uname_a_str =~ "Linux" ]]; then
        echo "Linux"
    elif [[ $uname_a_str =~ "Darwin" ]]; then
        echo "Darwin"
    else
        echo "Unsupported for platform ${uname_a_str}"
        exit 1
    fi
}

# more detailed: https://www.yuque.com/ncnn/cn/cvrt_linux_mac
function prepare_env() {
    # default
    echo "todo"

    # optional: caffe
    platform=$(get_platform)
    echo "platform: $platform"
    if [[ $platform =~ "Linux" ]]; then
        #sudo apt install -y libprotobuf-dev protobuf-compiler
        echo
    elif [[ $platform =~ "Darwin" ]]; then
	#brew install protobuf
        #sudo chown -R $(whoami) /usr/local
        #brew install -y libprotobuf-dev protobuf-compiler git
        echo
    fi

    # default
    if [ ! -d "./ncnn/" ];then
        git clone https://github.com/tencent/ncnn.git ncnn
    else
        echo "skipped git clone ncnn"
    fi
}

function main() {
    prepare_env
    platform=$(get_platform)

    # build
    cd ncnn

    if [[ $platform =~ "Linux" ]]; then
        ##### linux host system with gcc/g++
        mkdir -p build-host-gcc-linux
        pushd build-host-gcc-linux
        cmake -DCMAKE_TOOLCHAIN_FILE=../toolchains/host.gcc.toolchain.cmake ..
        make -j4
        make install
        make caffe2ncnn -j4
        make ncnnoptimize -j4
        popd
    elif [[ $platform =~ "Darwin" ]]; then
        ##### MacOS
        mkdir -p build-mac
        pushd build-mac
        cmake   -DNCNN_OPENMP=OFF \
                -DNCNN_OPENCV=ON \
                -DNCNN_BENCHMARK=ON \
                ..
        make -j 8
        make install
        make ncnnoptimize -j4
        make caffe2ncnn -j4
        popd
    fi


}

main

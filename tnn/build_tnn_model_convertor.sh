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

function prepare_env() {
    # default
    python3 -m pip install --upgrade pip
    pip3 install setuptools
    pip3 install onnx==1.6.0 onnxruntime numpy onnx-simplifier

    # optional: tensorflow
    pip3 install tensorflow==1.15.0
    pip3 install tf2onnx
    pip3 install onnxruntime

    # optional: caffe
    platform=$(get_platform)
    echo "platform: $platform"
    if [[ $platform =~ "Linux" ]]; then
        sudo apt-get install -y libprotobuf-dev protobuf-compiler git
    elif [[ $platform =~ "Darwin" ]]; then
        #sudo chown -R $(whoami) /usr/local
        #brew install -y libprotobuf-dev protobuf-compiler git
        echo
    fi

    # default
    if [ ! -d "./tnn/" ];then
        git clone https://github.com/Tencent/tnn.git
    else
        echo "skipped git clone tnn"
    fi
}

function main() {
    prepare_env

    # build
    cd tnn/tools/convert2tnn
    ./build.sh
}

main

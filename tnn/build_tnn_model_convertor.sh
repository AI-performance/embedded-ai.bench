#!/usr/bin/env bash
set -ex

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
    sudo apt-get install libprotobuf-dev protobuf-compiler
}

function main() {
    prepare_env

    # build
    cd tnn/tools/convert2tnn
    ./build.sh
}

main

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

# more detailed: https://www.yuque.com/mnn/cn/cvrt_linux_mac
function prepare_env() {
    # default
    echo "todo"

    # optional: caffe
    platform=$(get_platform)
    echo "platform: $platform"
    if [[ $platform =~ "Linux" ]]; then
        echo
    elif [[ $platform =~ "Darwin" ]]; then
        #sudo chown -R $(whoami) /usr/local
        #brew install -y libprotobuf-dev protobuf-compiler git
        echo
    fi

    # default
    if [ ! -d "./mnn/" ];then
        git clone https://github.com/alibaba/mnn.git mnn
    else
        echo "skipped git clone mnn"
    fi
}

function main() {
    prepare_env

    # build
    cd mnn
    ./schema/generate.sh
    mkdir build
    cd build
    cmake .. -DMNN_BUILD_CONVERTER=true && make -j4
}

main

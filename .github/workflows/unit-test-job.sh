#!/bin/bash
set -ex

sudo apt-get install -y android-tools-adb

#source ~/.bashrc
#conda init bash
#conda activate dev_env_py

PYDIR_LIST=("./core" "./utils")

if [ ! -d "./mnn/mnn" ]; then
    cd mnn && git clone https://github.com/alibaba/MNN.git mnn
fi

if [ ! -d "./tnn/tnn" ]; then
    cd tnn && git clone https://github.com/Tencent/TNN.git tnn
fi

if [ ! -d "./ncnn/ncnn" ]; then
    cd ncnn && git clone https://github.com/Tencent/NCNN.git ncnn
fi

# shellcheck disable=SC2068
for py_dir in ${PYDIR_LIST[@]}; do
    # shellcheck disable=SC2045
    for file in $(ls "${py_dir}"/*.py); do
        if [[ $py_dir =~ "__init__" ]]; then
            # do nothing
            date
        else
            echo "#>>>>>> Python Test for embededed-ai.bench"
            echo "#>>>>>> py file: ${file}"
            cd ${py_dir}
            echo $(basename ${file})
            python3 $(basename ${file})
            cd -
        fi
    done
done

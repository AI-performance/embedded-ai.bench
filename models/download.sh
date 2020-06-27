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
    platform=$(get_platform)
    echo $platform
    if [[ $platform =~ "Linux" ]]; then
        sudo apt update
        apt install -y wget unzip zip
    fi
}

##################################
# Prepare Caffe models
##################################
function caffe_model_urls() {
    links_for_caffe=( \ # mobilenetv1
                     "https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_deploy.prototxt" \
                     "https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet.caffemodel" \
                      \ # mobilenetv2
                     "https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_v2_deploy.prototxt" \
                     "https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_v2.caffemodel" \
                      \ # squeezenetv1.1
                     "https://raw.githubusercontent.com/DeepScale/SqueezeNet/master/SqueezeNet_v1.1/deploy.prototxt" \
                     "https://raw.githubusercontent.com/DeepScale/SqueezeNet/master/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel" \
                      \ # vgg16
                     "https://gist.githubusercontent.com/ksimonyan/211839e770f7b538e2d8/raw/0067c9b32f60362c74f4c445a080beed06b07eb3/VGG_ILSVRC_16_layers_deploy.prototxt" \
                     "http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_16_layers.caffemodel" \
                    )
    echo ${links_for_caffe[*]}
}

function rename_caffe_models() {
    # mobilenetv1
    mv mobilenet_deploy.prototxt caffe_mobilenetv1.prototxt
    mv mobilenet.caffemodel caffe_mobilenetv1.caffemodel

    # mobilenetv2
    mv mobilenet_v2_deploy.prototxt caffe_mobilenetv2.prototxt
    mv mobilenet_v2.caffemodel caffe_mobilenetv2.caffemodel

    # squeezenetv1.1
    mv deploy.prototxt caffe_squeezenetv1.1.prototxt
    mv squeezenet_v1.1.caffemodel caffe_squeezenetv1.1.caffemodel

    # vgg16
    mv VGG_ILSVRC_16_layers_deploy.prototxt caffe_vgg16.prototxt
    mv VGG_ILSVRC_16_layers.caffemodel caffe_vgg16.caffemodel
}

function prepare_caffe_models() {
    # download / unzip / rename caffe models
    links=$(caffe_model_urls)
    for url in ${links[@]}; do
        if [[ $url =~ "http" ]]; then
            echo "skip non-links: ${url}"
        else
            continue
        fi

        echo "prepare downloading $url"
        wget -cq $url
    done
    rename_caffe_models
    ls -lh caffe*
}

##################################
# TensorFlow models
##################################
function tensorflow_model_urls() {
    links_for_tensorflow=( \ # mobilenetv1
                          "https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz" \
                           \ # mobilenetv2
                          "https://storage.googleapis.com/mobilenet_v2/checkpoints/mobilenet_v2_1.0_224.tgz" \
                           \ # vgg16
                          "http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz" \
                         )
    echo ${links_for_tensorflow[*]}
}

function rename_tensorflow_models() {
    # TODO(ysh329): unzip models and rename with `tf` prefix
    # mobilenetv1
    tar -zxvf ./mobilenet_v1_1.0_224_frozen.tgz
    mv mobilenet_v1_1.0_224 tf_mobilenetv1

    # mobilenetv2
    tar -zxvf ./mobilenet_v2_1.0_224.tgz
    mkdir tf_mobilenetv2
    mv mobilenet_v2_1.0_224* ./tf_mobilenetv2/

    # vgg16
    tar -zxvf ./vgg_16_2016_08_28.tar.gz
    mkdir tf_vgg16
    mv vgg_16.ckpt ./tf_vgg16/tf_vgg16.ckpt
}

function prepare_tensorflow_models() {
    # TODO(ysh329): download / unzip / rename tensorflow models
    links=$(tensorflow_model_urls)
    for url in ${links[@]}; do
        if [[ $url =~ "http" ]]; then
            echo "skip non-links: ${url}"
        else
            continue
        fi

        echo "prepare downloading $url"
        wget -cq $url
    done
    rename_tensorflow_models
    ls -lh tf*
}


function main() {
    prepare_env
    prepare_caffe_models
    prepare_tensorflow_models

    ls -lh
}


##################################
# main
##################################
main

#!/usr/bin/env sh
set -ex

PROJECT_DIR=$(pwd)/../

function convert_to_tnn() {
    model_file=$1
    convert_type=""
    for (( i=0; i<${#model_file[@]}; i++ )) do
        model_dir="${PROJECT_DIR}/models/${model_file[i]}"
        convert_type=$(get_convert_type_from_file ${model_file[i]})
        echo "i=$i", ${model_file[i]}, $convert_type
    done
}

function get_convert_type_from_file() {
  in_model_file=$1
  convert_type=""
  if [[ $in_model_file =~ "caffe" ]]; then
      convert_type="caffe2tnn"
  elif [[ $in_model_file =~ "tf" ]]; then
      convert_type="tf2tnn"
  else
      echo "Unsupported convert from in_model_file:${in_model_file}"
      exit 1
  fi
  echo $convert_type
}

function convert_caffe() {
    models_dir="${PROJECT_DIR}/models"
    caffe_model_files=$(ls $models_dir | grep caffe)

    # check models num
    caffe_model_num=${#caffe_model_files[@]}
    if [[ $caffe_model_num == 0 ]]; then
        echo "No caffe models found"
        exit 1
    fi

    cd ./tnn/tools/convert2tnn/

    ##########################
    # do convert
    ##########################
    # caffe_mobilenetv1
    python3 ./converter.py caffe2tnn \
        ../../../../models/caffe_mobilenetv1.prototxt \
        ../../../../models/caffe_mobilenetv1.caffemodel \
        -optimize \
        -v v1.0 \
        -o ./../../../tnn-models/

    # caffe_mobilenetv2
    python3 ./converter.py caffe2tnn \
        ../../../../models/caffe_mobilenetv2.prototxt \
        ../../../../models/caffe_mobilenetv2.caffemodel \
        -optimize \
        -v v1.0 \
        -o ./../../../tnn-models/
}

function main() {
    convert_caffe
}

main

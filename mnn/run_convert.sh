#!/bin/bash
set -x

git clone https://github.com/ai-performance/mnn-models.git mnn-models

# convert Caffe
# ./MNNConvert -f CAFFE --modelFile XXX.caffemodel --prototxt XXX.prototxt --MNNModel XXX.mnn --bizCode biz
./mnn/build/MNNConvert \
  -f CAFFE \
  --modelFile ../models/caffe_mobilenetv1.caffemodel \
  --prototxt ../models/caffe_mobilenetv1.prototxt \
  --MNNModel ./mnn-models/caffe_mobilenetv1.mnn \
  --bizCode biz

./mnn/build/MNNConvert \
  -f CAFFE \
  --modelFile ../models/caffe_mobilenetv2.caffemodel \
  --prototxt ../models/caffe_mobilenetv2.prototxt \
  --MNNModel ./mnn-models/caffe_mobilenetv2.mnn \
  --bizCode biz

# convert tflite
# ./MNNConvert -f TFLITE --modelFile XXX.tflite --MNNModel XXX.mnn --bizCode biz
./mnn/build/MNNConvert \
  -f TFLITE \
  --modelFile ../models/tf_mobilenetv1/tf_mobilenetv1.tflite \
  --MNNModel ./mnn-models/tf_mobilenetv1.mnn \
  --bizCode biz

./mnn/build/MNNConvert \
  -f TFLITE \
  --modelFile ../models/tf_mobilenetv2/tf_mobilenetv2.tflite \
  --MNNModel ./mnn-models/tf_mobilenetv2.mnn \
  --bizCode biz

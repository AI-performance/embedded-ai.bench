#!/bin/bash
set -x

git clone https://github.com/ai-performance/ncnn-models.git ncnn-models

#./ncnn/build-host-gcc-linux/tools/ncnnoptimize 
#usage: ./ncnn/build-host-gcc-linux/tools/ncnnoptimize [inparam] [inbin] [outparam] [outbin] [flag]
#./ncnn/build-host-gcc-linux/tools/ncnnoptimize 

# ./ncnn/build-mac/tools/caffe/caffe2ncnn 
#Usage: ./ncnn/build-mac/tools/caffe/caffe2ncnn [caffeproto] [caffemodel] [ncnnproto] [ncnnbin] [quantizelevel] [int8scaletable]

# caffe_mobilenetv1: before convert, modify input as layer in caffe proto
./ncnn/build-mac/tools/caffe/caffe2ncnn \
  ../models/caffe_mobilenetv1.prototxt \
  ../models/caffe_mobilenetv1.caffemodel \
  ./caffe_mobilenetv1.param \
  ./caffe_mobilenetv1.bin

./ncnn/build-mac/tools/ncnnoptimize \
  ./caffe_mobilenetv1.param \
  ./caffe_mobilenetv1.bin \
  ./caffe_mobilenetv1.opt.param \
  ./caffe_mobilenetv1.opt.bin \
  65536

mv ./caffe_mobilenetv1*.opt.param ./ncnn-models/caffe_mobilenetv1.opt.param
mv ./caffe_mobilenetv1.opt.bin ./ncnn-models/caffe_mobilenetv1.opt.bin

# caffe_mobilenetv2
./ncnn/build-mac/tools/caffe/caffe2ncnn \
  ../models/caffe_mobilenetv2.prototxt \
  ../models/caffe_mobilenetv2.caffemodel \
  ./caffe_mobilenetv2.param \
  ./caffe_mobilenetv2.bin

./ncnn/build-mac/tools/ncnnoptimize \
  ./caffe_mobilenetv2.param \
  ./caffe_mobilenetv2.bin \
  ./caffe_mobilenetv2.opt.param \
  ./caffe_mobilenetv2.opt.bin \
  65536

mv ./caffe_mobilenetv2.opt.param ./ncnn-models/caffe_mobilenetv2.opt.param
mv ./caffe_mobilenetv2.opt.bin ./ncnn-models/caffe_mobilenetv2.opt.bin

echo "You should modifiy final layer name of param file as `output`"
echo "You should modifiy final layer name of param file as `output`"
echo "You should modifiy final layer name of param file as `output`"
echo "You should modifiy final layer name of param file as `output`"
echo "You should modifiy final layer name of param file as `output`"

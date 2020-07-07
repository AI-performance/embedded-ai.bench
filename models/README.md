# models

Original model stored for embedded-ai.bench.

## Usage

```shell script
./download.sh
```

## Detailed

| model | is_quant | framework | download link | note | 
|:-----:|:--------:|:---------:|--------|-----| 
|mobilenetv1| fp32 |caffe| [prototxt](https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_deploy.prototxt), [caffemodel](https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet.caffemodel) | [shicai/MobileNet-Caffe](https://github.com/shicai/MobileNet-Caffe) | 
|mobilenetv2| fp32 |caffe| [prototxt](https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_v2_deploy.prototxt), [caffemodel](https://raw.githubusercontent.com/shicai/MobileNet-Caffe/master/mobilenet_v2.caffemodel) | [shicai/MobileNet-Caffe](https://github.com/shicai/MobileNet-Caffe) | 
|squeezenetv1.1| fp32 |caffe| [prototxt](https://raw.githubusercontent.com/DeepScale/SqueezeNet/master/SqueezeNet_v1.1/deploy.prototxt), [caffemodel](https://github.com/DeepScale/SqueezeNet/raw/master/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel) | [DeepScale/SqueezeNet](https://github.com/DeepScale/SqueezeNet/tree/master/SqueezeNet_v1.1) |
|vgg16| fp32 |caffe| [prototxt](https://gist.githubusercontent.com/ksimonyan/211839e770f7b538e2d8/raw/0067c9b32f60362c74f4c445a080beed06b07eb3/VGG_ILSVRC_16_layers_deploy.prototxt), [caffemodel](http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_16_layers.caffemodel) | [ksimonyan](https://gist.github.com/ksimonyan/211839e770f7b538e2d8/) | 
|mobilenetv1| fp32 |tensorflow| [tflite&pb](https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224.tgz) | [tensorflow/models: Pre-trained Models](https://tensorflow.google.cn/lite/guide/hosted_models) | 
|mobilenetv2| fp32 |tensorflow| [tflite&pb](https://storage.googleapis.com/download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224.tgz) | [tensorflow/models: Pre-trained Models](https://tensorflow.google.cn/lite/guide/hosted_models)  | 
|squeezenetv1.1| fp32 |tensorflow| no provided | no provided |
|vgg16| fp32 |tensorflow| [vgg_16_2016_08_28.tar.gz](http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz) | [tensorflow/models: Pre-trained Models](https://github.com/tensorflow/models/tree/master/research/slim#Pretrained) |

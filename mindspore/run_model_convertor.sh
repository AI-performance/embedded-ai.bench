set -x

cd mindspore/output/mindspore-lite-0.7.0-converter-ubuntu/converter
# ./converter_lite
#usage:  [options]
# --bitNum=VALUE Weight quantization bitNum (default: 8)
# --config_file=VALUE Configuration for post-training. (default: )
# --convWeightQuantChannelThreshold=VALUE convWeightQuantChannelThreshold (default: 16)
# --fmk=VALUE Input model framework type. TFLITE | CAFFE | MS (default: )
# --formatTrans=VALUE whether transform format. true | false (default: t)
# --help print usage message (default: )
# --inferenceType=VALUE Real data type saved in output file, reserved param, NOT used for now. FLOAT | INT8 (default: FLOAT)
# --inputInferenceType=VALUE Input inference data type. FLOAT | INT8 (default: FLOAT)
# --mean=VALUE Mean value for aware-quantization (default: -0.5)
# --modelFile=VALUE Input model file path. TFLITE: *.tflite | CAFFE: *.prototxt | MS: *.mindir | ONNX: *.onnx (default: )
# --outputFile=VALUE Output model file path. Will add .ms automatically (default: )
# --quantSize=VALUE Weight quantization size threshold (default: 0)
# --quantType=VALUE Quantization Type. AwareTraining | PostTraining | WeightQuant (default: )
# --stdDev=VALUE Standard deviation value for aware-quantization (default: 128)
# --trainModel=VALUE whether the model is going to be trained on device. true | false (default: false)
# --weightFile=VALUE Input model weight file path. Needed when fmk is CAFFE. CAFFE: *.caffemodel (default: )

# note: https://www.mindspore.cn/lite/tutorial/zh-CN/master/use/converter_tool.html

prefix_path="/home/yuanshuai/code/tmp/embedded-ai.bench/"
# caffe
./converter_lite --fmk=CAFFE --modelFile=${prefix_path}/models/caffe_mobilenetv1.prototxt --weightFile=${prefix_path}/models/caffe_mobilenetv1.caffemodel --outputFile=caffe_mobilenetv1
./converter_lite --fmk=CAFFE --modelFile=${prefix_path}/models/caffe_mobilenetv2.prototxt --weightFile=${prefix_path}/models/caffe_mobilenetv2.caffemodel --outputFile=caffe_mobilenetv2

# tflite
./converter_lite --fmk=TFLITE --modelFile=${prefix_path}/models/tf_mobilenetv1/tf_mobilenetv1.tflite --outputFile=tf_mobilenetv1
./converter_lite --fmk=TFLITE --modelFile=${prefix_path}/models/tf_mobilenetv2/tf_mobilenetv2.tflite --outputFile=tf_mobilenetv2

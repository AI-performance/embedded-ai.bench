set -x

#git clone https://github.com/tensorflow/tensorflow.git
git clone https://gitee.com/mirrors/tensorflow.git tflite
cd tflite

bazel build -c opt \
  --config=android_arm64 \
  tensorflow/lite/tools/benchmark:benchmark_model

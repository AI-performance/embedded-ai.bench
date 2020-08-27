set -x

# ref: https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/android
git clone https://gitee.com/mirrors/tensorflow.git tflite
cd tflite


sudo apt install curl gnupg
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install bazel
sudo apt update && sudo apt full-upgrade
sudo apt update && sudo apt install bazel-3.1.0




bazel build -c opt \
  --config=android_arm64 \
  tensorflow/lite/tools/benchmark:benchmark_model

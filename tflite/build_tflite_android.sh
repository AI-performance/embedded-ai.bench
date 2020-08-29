set -x

# ref: https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/android
git clone https://gitee.com/mirrors/tensorflow.git tflite

cd tflite

apt update
apt install -y curl gnupg



#curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
#echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
#sudo apt update && sudo apt install bazel
#sudo apt update && sudo apt full-upgrade
#sudo apt update && sudo apt install bazel-3.1.0
#apt install bazel
#apt install -y bazel-3.1.0
cd "/usr/local/lib/bazel/bin" && curl -LO https://releases.bazel.build/3.1.0/release/bazel-3.1.0-linux-x86_64 && chmod +x bazel-3.1.0-linux-x86_64
cd -


./configure
# android: y
# ndk path: /opt/android-ndk-r17c/

bazel build -c opt \
  --config=android_arm \
  tensorflow/lite/tools/benchmark:benchmark_model
# bazel-tflite/bazel-out/arm64-v8a-opt/bin/tensorflow/lite/tools/benchmark/benchmark_model


bazel build -c opt \
  --config=android_arm64 \
  tensorflow/lite/tools/benchmark:benchmark_model
# bazel-tflite/bazel-out/arm64-v8a-opt/bin/tensorflow/lite/tools/benchmark/benchmark_model

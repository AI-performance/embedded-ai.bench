#!/usr/bin/env bash
# below from tensorflow-repo/.bazelrc
# Android configs. Bazel needs to have --cpu and --fat_apk_cpu both set to the
# target CPU to build transient dependencies correctly. See
# https://docs.bazel.build/versions/master/user-manual.html#flag--fat_apk_cpu
#build:android --crosstool_top=//external:android/crosstool
#build:android --host_crosstool_top=@bazel_tools//tools/cpp:toolchain
#build:android_arm --config=android
#build:android_arm --cpu=armeabi-v7a
#build:android_arm --fat_apk_cpu=armeabi-v7a
#build:android_arm64 --config=android
#build:android_arm64 --cpu=arm64-v8a
#build:android_arm64 --fat_apk_cpu=arm64-v8a
BUILD_CONFIG="android"
BUILD_ARM_VERSION_LIST=("arm64-v8a" "armeabi-v7a")
BUILD_TARGET="benchmark_model"
TFLITE_DEVICE_PATH="/data/local/tmp/tflite"
./configure
adb shell "mkdir ${DEVICE_PATH}"
# build ${BUILD_TARGET}
for BUILD_ARM_VERSION in ${BUILD_ARM_VERSION_LIST[@]}; do
    echo "====== ${BUILD_ARM_VERSION} ======"
    # build
    bazel build -c opt \
      --config=android_arm \
      --cxxopt='--std=c++11' \
      --config=android \
      --cpu=${BUILD_ARM_VERSION} \
      --fat_apk_cpu=${BUILD_ARM_VERSION} \
      tensorflow/lite/tools/benchmark:${BUILD_TARGET}
    # save
    cp ./bazel-bin/tensorflow/lite/tools/benchmark/${BUILD_TARGET} ./${BUILD_ARM_VERSION}_${BUILD_TARGET}
done
#!/usr/bin/env bash
# https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/tools/benchmark
TFLITE_DEVICE_PATH="/data/local/tmp/tflite"
adb shell "mkdir ${TFLITE_DEVICE_PATH}"
BUILD_ARM_VERSION_LIST=("arm64-v8a" "armeabi-v7a")
BUILD_TARGET="benchmark_model"
# Download tflite model:https://www.tensorflow.org/lite/guide/hosted_models
MODEL_URL_LIST=("https://storage.googleapis.com/download.tensorflow.org/models/tflite/model_zoo/upload_20180427/densenet_2018_04_27.tgz"
                "https://storage.googleapis.com/download.tensorflow.org/models/tflite/model_zoo/upload_20180427/squeezenet_2018_04_27.tgz"
                "https://storage.cloud.google.com/download.tensorflow.org/models/tflite/mnasnet_1.0_224_09_07_2018.tgz"
                "https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_02_22/mobilenet_v1_1.0_224.tgz"
                "https://storage.googleapis.com/download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224.tgz"
                "https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224_quant.tgz"
                "https://storage.googleapis.com/download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz")
MODEL_HOST_PATH="./tfmodel"
MODEL_ZIP_SUFFIX_NAME=".tgz"
MODEL_UNZIP_SUFFIX_NAME=".tflite"
MODEL_DEVICE_PATH="${TFLITE_DEVICE_PATH}/tfmodel"
mkdir ${MODEL_HOST_PATH}
cd ${MODEL_HOST_PATH}
# donwload tfmodel
for MODEL_URL in ${MODEL_URL_LIST[@]}; do
    echo "[INFO] Download ${MODEL_URL}"
    echo #wget -c ${MODEL_URL} ${MODEL_HOST_PATH}/
done
# unzip model file
echo "[INFO] unzip model"
MODEL_ZIPPED_LIST=$(ls | grep ${MODEL_ZIP_SUFFIX_NAME})
for MODEL_FILE in ${MODEL_ZIPPED_LIST[@]}; do
    echo "[INFO] Unzip model file: ${MODEL_FILE}"
    tar -zxvf ${MODEL_FILE}
done
# unzip model file
adb shell mkdir ${MODEL_DEVICE_PATH}
MODEL_NAME_LIST=$(ls | grep ${MODEL_UNZIP_SUFFIX_NAME})
for TFLITE_MODEL_FILE in ${MODEL_NAME_LIST[@]}; do
    echo "[INFO] tflite model file: ${TFLITE_MODEL_FILE}"
    adb push --sync ${TFLITE_MODEL_FILE} ${MODEL_DEVICE_PATH}
done
adb push --sync "mnasnet_1.0_224/mnasnet_1.0_224.tflite" ${MODEL_DEVICE_PATH}
cd ..
# push
for BUILD_ARM_VERSION in ${BUILD_ARM_VERSION_LIST[@]}; do
    echo "====== ${BUILD_ARM_VERSION} ======"
    # push
    echo "adb push --sync ./${BUILD_ARM_VERSION}_${BUILD_TARGET} ${TFLITE_DEVICE_PATH}"
    adb push --sync "./${BUILD_ARM_VERSION}_${BUILD_TARGET}" ${TFLITE_DEVICE_PATH}
done
# run benchmark
echo "[INFO] run benchmark"
WARMUP_RUNS="4"
NUM_RUNS=10
USE_GPU_LIST=(false) #(false true)
NUM_THREADS_LIST=("1" "2" "4")
MODEL_NAME_LIST=$(adb shell "cd ${MODEL_DEVICE_PATH}; ls *.tflite")
for BUILD_ARM_VERSION in ${BUILD_ARM_VERSION_LIST[@]}; do
    echo "[INFO] ====== run benchmark of ${BUILD_ARM_VERSION} ======"
    adb shell "chmod +x ${TFLITE_DEVICE_PATH}/${BUILD_ARM_VERSION}_${BUILD_TARGET}"
    for MODEL_NAME in ${MODEL_NAME_LIST[@]}; do
        for USE_GPU in ${USE_GPU_LIST[@]}; do
            if [[ ${USE_GPU} == false ]]; then
                for NUM_THREADS in ${NUM_THREADS_LIST[@]}; do
                    echo "echo '[INFO] ==== ${BUILD_ARM_VERSION} USE_GPU:${USE_GPU}-${NUM_THREADS} ${MODEL_DEVICE_PATH}/${MODEL_NAME} ===='"
                    adb shell "${TFLITE_DEVICE_PATH}/${BUILD_ARM_VERSION}_${BUILD_TARGET} --graph=${MODEL_DEVICE_PATH}/${MODEL_NAME} --num_threads=${NUM_THREADS} --warmup_runs=${WARMUP_RUNS} --num_runs=${NUM_RUNS} --use_gpu=${USE_GPU}"
                done
            fi
            if [[ ${USE_GPU} == true ]]; then
                NUM_THREADS=-1
                echo "[INFO] ==== ${BUILD_ARM_VERSION} USE_GPU:${USE_GPU}-${NUM_THREADS} ${MODEL_DEVICE_PATH}/${MODEL_NAME} ===="
                adb shell "${TFLITE_DEVICE_PATH}/${BUILD_ARM_VERSION}_${BUILD_TARGET} \
                           --graph=${MODEL_DEVICE_PATH}/${MODEL_NAME} \
                           --warmup_runs=${WARMUP_RUNS} \
                           --num_runs=${NUM_RUNS} \
                           --use_gpu=${USE_GPU}"
            fi
        done # USE_GPU_LIST
    done # MODEL_NAME_LIST
done # BUILD_ARM_VERSION_LIST
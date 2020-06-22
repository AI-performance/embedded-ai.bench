#!/usr/bin/env bash

# init params
HOST_BUILD_PATH_LIST=("build-android-armv7" \
                      "build-android-aarch64" \
                      "build-android-armv7-vulkan" \
                      "build-android-aarch64-vulkan")
#HOST_BUILD_PATH_LIST=("build-android-aarch64-vulkan")

NCNN_DEVICE_PATH="/data/local/tmp/ncnn"
NCNN_LOOP_COUNT="4" #"10"

# cpu setting
NCNN_NUM_THREADS_LIST=("1" "2" "4")
NCNN_POWERSAVE="2"
NCNN_CPU_DEVICE="-1"

# gpu setting
NCNN_CPU_NUM_THREADS_ON_GPU_DEVICE="1"
NCNN_GPU_DEVICE="0"
NCNN_GPU_PATTERN="vulkan"

# push benchmark
adb shell "mkdir ${NCNN_DEVICE_PATH}"
adb push --sync ./benchmark/*.param ${NCNN_DEVICE_PATH}

# run benchmark
for HOST_BUILD_PATH in ${HOST_BUILD_PATH_LIST[@]}; do
    echo "---- HOST_BUILD_PATH:${HOST_BUILD_PATH} ----"
    adb push --sync ./${HOST_BUILD_PATH}/benchmark/benchncnn ${NCNN_DEVICE_PATH}

    if [[ ${HOST_BUILD_PATH} =~ ${NCNN_GPU_PATTERN} ]]
    then # do gpu: enable gpu
        NCNN_GPU_DEVICE="0"
        adb shell "cd ${NCNN_DEVICE_PATH}; ${NCNN_DEVICE_PATH}/benchncnn ${NCNN_LOOP_COUNT} ${NCNN_CPU_NUM_THREADS_ON_GPU_DEVICE} ${NCNN_POWERSAVE} ${NCNN_GPU_DEVICE}"
        #echo "adb shell cd ${NCNN_DEVICE_PATH}; ${NCNN_DEVICE_PATH}/benchncnn ${NCNN_LOOP_COUNT} ${NCNN_CPU_NUM_THREADS_ON_GPU_DEVICE} ${NCNN_POWERSAVE} ${NCNN_GPU_DEVICE}"
    else # do cpu
        for NCNN_NUM_THREADS in ${NCNN_NUM_THREADS_LIST[@]}; do
            adb shell "cd ${NCNN_DEVICE_PATH}; ${NCNN_DEVICE_PATH}/benchncnn ${NCNN_LOOP_COUNT} ${NCNN_NUM_THREADS} ${NCNN_POWERSAVE} ${NCNN_CPU_DEVICE}"
            #echo "adb shell cd ${NCNN_DEVICE_PATH}; ${NCNN_DEVICE_PATH}/benchncnn ${NCNN_LOOP_COUNT} ${NCNN_NUM_THREADS} ${NCNN_POWERSAVE} ${NCNN_CPU_DEVICE}"
            #echo "${NCNN_DEVICE_PATH}/benchncnn ${NCNN_LOOP_COUNT} ${NCNN_NUM_THREADS} ${NCNN_POWERSAVE} ${NCNN_CPU_DEVICE}"
        done
    fi
    echo
done
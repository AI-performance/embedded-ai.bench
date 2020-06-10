#set -e

#SERIAL_NUM_LIST="7f1446bd" # 845
#serial_num="17c3cc34" # 855
#serial_num="93fe992b" #835
#SERIAL_NUM_LIST=("93fe992b") # "7f1446bd" "17c3cc34")
#SERIAL_NUM_LIST=("8N1945EE19446352")
SERIAL_NUM_LIST=("H5X6R20514029505") #820
#SERIAL_NUM_LIST=("7HX5T19929012679") # 990
DEVICE_BACKEND_LIST=("ARM" "OPENCL")
ARM_CPU_THREAD_LIST=(1 2 4)


rm TNNTest libTNN.so
wget -c http://10.87.145.34:8888/code/tnn-test/scripts/build32/test/TNNTest
wget -c http://10.87.145.34:8888/code/tnn-test/scripts/release/armeabi-v7a/libTNN.so
# run bench
for serial_num in ${SERIAL_NUM_LIST[@]}; do
    adb -s ${serial_num} shell mkdir -p /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} shell rm /data/local/tmp/embeded-ai-benchmark/tnn/TNNTest

    adb -s ${serial_num} push ./TNNTest /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ./libTNN.so /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ./libTNN.a /data/local/tmp/embeded-ai-benchmark/tnn/

    adb -s ${serial_num} shell chmod +x /data/local/tmp/embeded-ai-benchmark/tnn/TNNTest

    target_soc=$(adb -s ${serial_num} shell getprop | grep "ro.board.platform")
    echo "##########################################################"
    echo "# ${serial_num} | ${target_soc} #"
    echo "##########################################################"

#Parameter -mp is not set
#    -h                      print a usage message.
#    -mt "<model type>"    specify model type: TNN, OPENVINO, COREML, SNPE.
#    -mp "<model path>"    specify model path: tnn proto path, openvino xml path, coreml mlmodel path, snpe dlc path.
#    -dt "<device type>"   specify tnn device type: CPU, X86, ARM, CUDA, METAL, OPENCL, default is CPU.
#    -lp "<library path>"  specify tnn NetworkConfig library_path. For metal, it is the tnn.metallib full path
#    -ic "<number>"        iterations count (default 1).
#    -wc "<number>"        warm up count (default 0).
#    -ip "<path>"          input file path
#    -op "<path>"          output file path
#    -dl "<device list>"   device list(eg: 0,1,2,3)
#    -th "<thread umber>"  cpu thread num(eg: 0,1,2,3, default 1)
#    -it "<input type>"    input format(0: nchw float, 1:bgr u8, 2, gray u8)
#    -fc "<format for compare>"output format for comparison
#    -pr "<precision >"    compute precision(HIGH, NORMAL, LOW)

#    adb -s ${serial_num} push ../../private/ncnn/caffe_mobilenetv1.bin /data/local/tmp/embeded-ai-benchmark/tnn/
#    adb -s ${serial_num} push ../../private/ncnn/caffe_mobilenetv1.param /data/local/tmp/embeded-ai-benchmark/tnn/
#    adb -s ${serial_num} push ../../private/ncnn/caffe_mobilenetv2.bin /data/local/tmp/embeded-ai-benchmark/tnn/
#    adb -s ${serial_num} push ../../private/ncnn/caffe_mobilenetv2.param /data/local/tmp/embeded-ai-benchmark/tnn/

    adb -s ${serial_num} push ../../private/tnn-models/caffe_mobilenetv1.opt.tnnproto /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/caffe_mobilenetv1.opt.tnnmodel /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/caffe_mobilenetv2.opt.tnnproto /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/caffe_mobilenetv2.opt.tnnmodel /data/local/tmp/embeded-ai-benchmark/tnn/

    adb -s ${serial_num} push ../../private/tnn-models/tf_mobilenetv1.opt.tnnproto /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/tf_mobilenetv1.opt.tnnmodel /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/tf_mobilenetv2.opt.tnnproto /data/local/tmp/embeded-ai-benchmark/tnn/
    adb -s ${serial_num} push ../../private/tnn-models/tf_mobilenetv2.opt.tnnmodel /data/local/tmp/embeded-ai-benchmark/tnn/

    for device_backend in ${DEVICE_BACKEND_LIST[@]}; do
        MODEL_PROTO_LIST=$(adb -s ${serial_num} shell ls /data/local/tmp/embeded-ai-benchmark/tnn/*.tnnproto)
        for model_proto_dir in ${MODEL_PROTO_LIST[@]}; do
            echo "======================================================================="
            echo "serial_num:${serial_num}"
            echo "target_soc:${target_soc}"
            echo "device_backend:${device_backend}"
            echo "thread_num:${thread_num}"
            echo "model_proto_dir:${model_proto_dir}"

            adb -s ${serial_num} shell "export LD_LIBRARY_PATH=/data/local/tmp/embeded-ai-benchmark/tnn/; /data/local/tmp/embeded-ai-benchmark/tnn/TNNTest \
              -mt TNN \
              -mp ${model_proto_dir} \
              -dt ${device_backend} \
              -ic 100 \
              -wc 20 \
              -th ${thread_num}"
        done
    done
done

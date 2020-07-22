adb shell mkdir /data/local/tmp/mnn/
adb push ./mnn/project/android/build_32/libMNN.so /data/local/tmp/mnn/libMNN.so
adb push ./mnn/project/android/build_32/libMNN_Express.so /data/local/tmp/mnn/libMNN_Express.so
adb push ./mnn/project/android/build_32/MNNV2Basic.out /data/local/tmp/mnn/MNNV2Basic.out
adb push 

adb shell chmod +x /data/local/tmp/mnn/MNNV2Basic.out

mnn_models=$(ls mnn-models/*.mnn)
for model_dir in ${mnn_models[@]}; do
    adb push $model_dir /data/local/tmp/mnn/$model_dir
done

mnn_models_on_devices=$(adb shell ls /data/local/tmp/mnn/mnn-models/)
for model_dir in ${mnn_models_on_devices[@]}; do
    adb push $model_dir /data/local/tmp/mnn/mnn-models/${model_dir}
    adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mnn/;
               /data/local/tmp/mnn/MNNV2Basic.out \
               /data/local/tmp/mnn/mnn-models/${model_dir} \
               10 0 0 1 "
done
# Arguments: model.MNN runTimes saveAllTensors forwardType numberThread size
# forwardtype有0->CPU，1->Metal，3->OpenCL，6->OpenGL，7->Vulkan


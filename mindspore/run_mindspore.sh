set -x

#adb shell rm -rf /data/local/tmp/mindspore/
adb shell mkdir -p /data/local/tmp/mindspore/

adb push ./benchmark/benchmark /data/local/tmp/mindspore/benchmark
adb push ./lib/libmindspore-lite.so /data/local/tmp/mindspore/libmindspore-lite.so
adb push ./lib/liboptimize.so /data/local/tmp/mindspore/liboptimize.so
adb push ./lib/libc++_shared.so /data/local/tmp/mindspore/libc++_shared.so

adb push /Users/yuanshuai06/Baidu/code/dl-inference-benchmark/mindspore/mindspore-models/tf_mobilenetv1.ms /data/local/tmp/mindspore/tf_mobilenetv1.ms
adb push /Users/yuanshuai06/Baidu/code/dl-inference-benchmark/mindspore/mindspore-models/tf_mobilenetv2.ms /data/local/tmp/mindspore/tf_mobilenetv2.ms
adb push /Users/yuanshuai06/Baidu/code/dl-inference-benchmark/mindspore/mindspore-models/caffe_mobilenetv1.ms /data/local/tmp/mindspore/caffe_mobilenetv1.ms
adb push /Users/yuanshuai06/Baidu/code/dl-inference-benchmark/mindspore/mindspore-models/caffe_mobilenetv2.ms /data/local/tmp/mindspore/caffe_mobilenetv2.ms

adb shell chmod +x /data/local/tmp/mindspore/benchmark

# https://www.mindspore.cn/lite/tutorial/zh-CN/master/use/evaluating_the_model.html
#adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; \
#  /data/local/tmp/mindspore/benchmark \
#  --modelPath=<xxx> \
#  --device=<CPU|GPU> \
#  --cpuBindMode=<-1:midcore, 1: bigcore, 0:nobind> \
#  --numThreads=<2> \
#  --loopCount=10 \
#  --warmUpLoopCount=3 \
#  --fp16Priority=<false|true>"

adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; \
  /data/local/tmp/mindspore/benchmark \
  --modelPath=/data/local/tmp/mindspore/tf_mobilenetv1.ms \
  --device=CPU \
  --cpuBindMode=1 \
  --numThreads=1 \
  --loopCount=1000 \
  --warmUpLoopCount=20 \
  --fp16Priority=true"

adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; \
  /data/local/tmp/mindspore/benchmark \
  --modelPath=/data/local/tmp/mindspore/tf_mobilenetv2.ms \
  --device=CPU \
  --cpuBindMode=1 \
  --numThreads=1 \
  --loopCount=1000 \
  --warmUpLoopCount=20 \
  --fp16Priority=true"

adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; \
  /data/local/tmp/mindspore/benchmark \
  --modelPath=/data/local/tmp/mindspore/caffe_mobilenetv1.ms \
  --device=CPU \
  --cpuBindMode=1 \
  --numThreads=1 \
  --loopCount=1000 \
  --warmUpLoopCount=20 \
  --fp16Priority=true"

adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; \
  /data/local/tmp/mindspore/benchmark \
  --modelPath=/data/local/tmp/mindspore/caffe_mobilenetv2.ms \
  --device=CPU \
  --cpuBindMode=1 \
  --numThreads=1 \
  --loopCount=1000 \
  --warmUpLoopCount=20 \
  --fp16Priority=true"

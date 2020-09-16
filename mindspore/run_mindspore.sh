set -x

adb shell rm -rf /data/local/tmp/mindspore/
adb shell mkdir -p /data/local/tmp/mindspore/

adb push ./benchmark/benchmark /data/local/tmp/mindspore/benchmark
adb push ./lib/libmindspore-lite.so /data/local/tmp/mindspore/libmindspore-lite.so
adb push ./lib/liboptimize.so /data/local/tmp/mindspore/liboptimize.so
adb push ./lib/libc++_shared.so /data/local/tmp/mindspore/libc++_shared.so

adb shell chmod +x /data/local/tmp/mindspore/benchmark
adb shell "export LD_LIBRARY_PATH=/data/local/tmp/mindspore/; /data/local/tmp/mindspore/benchmark"

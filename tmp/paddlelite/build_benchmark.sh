# (paddle-lite根目录下) 下载benchmark模型
wget -c https://paddle-inference-dist.bj.bcebos.com/lite_benchmark%2Fbenchmark_models.tar.gz
tar -zxvf lite_benchmark%2Fbenchmark_models.tar.gz

# 编译benchmark
./lite/tools/ci_build.sh \
  --arm_os="android" \
  --arm_abi="armv8" \
  --arm_lang="gcc " \
  build_arm

# adb上传benchmark的bin和模型
adb shell mkdir /data/local/tmp/paddlelite
adb push -p ./benchmark_models/ /data/local/tmp/paddlelite/                                                                
adb push -p ./build.lite.android.armv8.gcc/lite/api/benchmark_bin /data/local/tmp/paddlelite/
 
MODEL_LIST=$(ls ./benchmark_models)
REPEATS_NUM=50
WARMUP_NUM=10
THREADS_NUM_LIST=(1 2 4)

# 执行benchmark 
for model_name in ${MODEL_LIST[@]}; do
    for thread_num in ${THREADS_NUM_LIST[@]}; do
        echo "${model_name}-${thread_num}"
        adb shell /data/local/tmp/paddlelite/benchmark_bin \
           --model_dir=/data/local/tmp/paddlelite/${model_name} \
           --repeats=${REPEATS_NUM} \
           --warmup=${WARMUP_NUM} \
           --threads=${thread_num} \
           --result_filename=/data/local/tmp/paddlelite/benchmark.log
    done
done

# 拉取benchmark日志
adb pull /data/local/tmp/paddlelite/benchmark.log .
cat benchmark.log
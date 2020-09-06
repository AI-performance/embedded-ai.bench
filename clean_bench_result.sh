set -x

mkdir -p bench_backup/ncnn
mkdir -p bench_backup/mnn
mkdir -p bench_backup/tnn
mkdir -p bench_backup/tflite

mv ./ncnn/*.csv bench_backup/ncnn
mv ./tnn/*.csv bench_backup/tnn
mv ./mnn/*.csv bench_backup/mnn
mv ./tflite/*.csv bench_backup/tflite

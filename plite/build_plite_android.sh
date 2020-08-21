set -x

git clone https://github.com/PaddlePaddle/Paddle-Lite.git plite

cd plite

./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv7 \
 --arm_lang=clang \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv8 \
 --arm_lang=clang \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

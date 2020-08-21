set -x

git clone https://github.com/PaddlePaddle/Paddle-Lite.git plite
cd plite

# download Android NDK for linux-x86_64
#    note: Skip this step if NDK installed
#    ref: https://developer.android.com/ndk/downloads
readonly ANDROID_NDK_HOME=/opt/android-ndk-r17c
if [ ! -d ${ANDROID_NDK_HOME} ]; then
    cd /tmp && wget -c https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip
    cd /opt && unzip /tmp/android-ndk-r17c-linux-x86_64.zip
else
    echo "local ${ANDROID_NDK_HOME} existed"
fi
export ANDROID_NDK=${ANDROID_NDK_HOME}
cd -

# build android armv7
./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv7 \
 --arm_lang=clang \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

# build android armv8
./lite/tools/build.sh \
 --arm_os=android \
 --arm_abi=armv8 \
 --arm_lang=clang \
 --build_extra=ON \
 --build_cv=ON \
 tiny_publish

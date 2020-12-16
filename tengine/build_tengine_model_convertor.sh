set -x

git clone https://github.com/OAID/Tengine.git tengine
cd tengine
git checkout tengine-lite

# build model convertor
mkdir build-convertor
cd build-convertor
cmake -DCMAKE_TOOLCHAIN_FILE=../toolchains/x86.gcc.toolchain.cmake ..
make -j4 && make install

# for linux env
#wget -c https://github.com/gcc-mirror/gcc/archive/basepoints/gcc-8.tar.gz
#tar -zxvf gcc-8.tar.gz

# gcc
#wget -c https://mirrors.ustc.edu.cn/gnu/gcc/gcc-8.3.0/gcc-8.3.0.tar.xz
#tar xvf gcc-8.3.0.tar.xz
#cd ./gcc-8.3.0
#./contrib/download_prerequisites
#mkdir build-gcc-8.3.0
#cd build-gcc-8.3.0
#../configure --enable-checking=release --enable-languages=c,c++ --disable-multilib --prefix=/opt/gcc-8.3
# make 
# make install
apt-get install -y software-properties-common python-software-properties
add-apt-repository ppa:ubuntu-toolchain-r/test
apt-get update
apt-get install -y gcc-8 g++-8

update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 50


# preq
apt-get install -y autoconf automake libtool

# build
cd mindspore
bash build.sh -I x86_64 -j30

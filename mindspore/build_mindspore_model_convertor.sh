# for linux env
apt-get install -y autoconf automake libtool

cd mindspore
bash build.sh -I x86_64 -j30

#!/bin/bash
set -x

git clone https://github.com/ai-performance/ncnn-models.git ncnn-models

#./ncnn/build-host-gcc-linux/tools/ncnnoptimize 
#usage: ./ncnn/build-host-gcc-linux/tools/ncnnoptimize [inparam] [inbin] [outparam] [outbin] [flag]
./ncnn/build-host-gcc-linux/tools/ncnnoptimize 

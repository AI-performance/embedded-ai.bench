# TNN

Only support build android.

## build.sh

Build Android armv7 && armv8:

```shell
./build.sh
```

## benchmark

See `<embedded-ai.bench>/bench.py` and run it.

## Appendix

```shell
#Parameter -mp is not set
#    -h                      print a usage message.
#    -mt "<model type>"    specify model type: TNN, OPENVINO, COREML, SNPE.
#    -mp "<model path>"    specify model path: tnn proto path, openvino xml path, coreml mlmodel path, snpe dlc path.
#    -dt "<device type>"   specify tnn device type: CPU, X86, ARM, CUDA, METAL, OPENCL, default is CPU.
#    -lp "<library path>"  specify tnn NetworkConfig library_path. For metal, it is the tnn.metallib full path
#    -ic "<number>"        iterations count (default 1).
#    -wc "<number>"        warm up count (default 0).
#    -ip "<path>"          input file path
#    -op "<path>"          output file path
#    -dl "<device list>"   device list(eg: 0,1,2,3)
#    -th "<thread umber>"  cpu thread num(eg: 0,1,2,3, default 1)
#    -it "<input type>"    input format(0: nchw float, 1:bgr u8, 2, gray u8)
#    -fc "<format for compare>"output format for comparison
#    -pr "<precision >"    compute precision(HIGH, NORMAL, LOW)
```

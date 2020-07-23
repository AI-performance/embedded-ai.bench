#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from core.engine import Engine
from core.global_config import create_config


def bench(name):
    if name is None:
        return
    config_dict = create_config(name)
    engine = Engine(config_dict)

    model_dict = engine.prepare_models()
    device_dict = engine.prepare_devices()
    engine.set_config("model_dict", model_dict)
    engine.set_config("device_dict", device_dict)

    engine.prepare_models_for_devices()
    engine.prepare_benchmark_assets_for_devices()

    bench_dict = engine.run_bench()

    bench_str_list = engine.generate_benchmark_summary(bench_dict)
    engine.write_list_to_file(bench_str_list)


def main():
    bench("tnn")
    bench("ncnn")
    bench("mnn")


if __name__ == "__main__":
    main()

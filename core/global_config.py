#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import unittest

sys.path.append("..")
from utils.log import LoggerCreator  # noqa

log_enable_debug = True
logger_creator = LoggerCreator(log_enable_debug)
logger = logger_creator.create_logger()


def create_config(framework_name):
    benchmark_platform = ["android-armv7", "android-armv8"]
    config = dict()
    if framework_name == "tnn":
        # note(ysh329):
        # https://github.com/Tencent/TNN/blob/master/doc/cn/user/test.md
        config["work_dir"] = "./{}".format(framework_name)
        config["model_repo"] = "https://gitee.com/yuens/{}-models.git".format(
            framework_name
        )
        config["model_type_keyword"] = framework_name
        # complete model version during `prepare_models`
        config["model_repo_version"] = -1
        config["model_repo_version_extra"] = -1
        config["model_repo_branch"] = -1
        config["model_repo_commit_id"] = -1
        config["device_work_dir"] = "/data/local/tmp/ai-performance/{}".format(
            framework_name
        )
        # complete framework version
        config["framework_repo_branch"] = -1
        config["framework_repo_commit_id"] = -1
        config["framework_name"] = framework_name
        config["benchmark_platform"] = benchmark_platform
        for pidx in range(len(benchmark_platform)):
            platform = benchmark_platform[pidx]
            config[platform] = dict()
            config[platform][
                "shared_lib"
            ] = "./tnn/scripts/build{}/libTNN.so".format(  # noqa
                32 if "v7" in platform else 64
            )
            config[platform][
                "benchmark_bin"
            ] = "./tnn/scripts/build{}/test/TNNTest".format(
                32 if "v7" in platform else 64
            )
        config["repeats"] = 100
        config["warmup"] = 20
        config["support_backend"] = ["ARM", "OPENCL"]
        config["is_cpu_backend"] = (
            lambda b: b.upper() == "CPU" or b.upper() == "ARM"
        )  # noqa
        config["cpu_thread_num"] = [1, 2, 4]
        # power_mode: "big_cores" # "little_cores", "no_bind"
        config["power_mode"] = "big_cores"
        config["bench_cmd_pattern"] = (
            'adb -s {serial_num} shell "export LD_LIBRARY_PATH={device_work_dir}; {'  # noqa
            "device_benchmark_bin} -mt {model_type} -mp {model_dir} -dt {backend} -ic {"  # noqa
            'repeats} -wc {warmup} -th {thread_num} -dl {bind_cpu_idx}" '
        )
    elif framework_name == "ncnn":
        # note(ysh329):
        # https://github.com/Tencent/ncnn/tree/master/benchmark/README.md
        config["work_dir"] = "./{}".format(framework_name)
        config[
            "model_repo"
        ] = "https://github.com/ai-performance/{}-models.git".format(  # noqa
            framework_name
        )
        config["model_type_keyword"] = "param"
        # complete model version during `prepare_models`
        config["model_repo_version"] = -1
        config["model_repo_version_extra"] = -1
        config["model_repo_branch"] = -1
        config["model_repo_commit_id"] = -1
        config["device_work_dir"] = "/data/local/tmp/ai-performance/{}".format(
            framework_name
        )
        # complete framework version
        config["framework_repo_branch"] = -1
        config["framework_repo_commit_id"] = -1
        config["framework_name"] = framework_name
        config["benchmark_platform"] = benchmark_platform
        for pidx in range(len(benchmark_platform)):
            platform = benchmark_platform[pidx]
            config[platform] = dict()
            config[platform][
                "benchmark_bin"
            ] = "./ncnn/build-android-{}/benchmark/benchncnn".format(
                "armv7" if "v7" in platform else "aarch64"
            )
            config[platform]["shared_lib"] = "./ncnn/README.md"
        config["repeats"] = 100
        config["warmup"] = 20

        # gpu device: -1=cpu-only, 0=gpu0, 1=gpu1 ...
        def support_backend_id(backend="ARM"):
            if backend.upper() == "ARM":
                return -1
            elif backend.upper() == "VULKAN":
                return 0
            else:
                logger.error("Unsupported backend: {}".format(backend))
                logger.error("use ARM instead")
                return -1

        config["support_backends"] = ["ARM", "VULKAN"]
        config["backend_id_to_str_dict"] = {"-1": "ARM", "0": "VULKAN"}
        config["is_cpu_backend"] = lambda backend_id: str(backend_id) == "-1"
        config["support_backend"] = list(
            map(support_backend_id, config["support_backends"])
        )
        config["cpu_thread_num"] = [1, 2, 4]

        # 0=all cores, 1=little cores only, 2=big cores only
        def power_mode_id(mode="big_cores"):
            if mode == "big_cores":
                return 2
            elif mode == "litte_cores":
                return 1
            elif mode == "all_cores":
                return 0
            else:
                logger.error("Unsupported power mode:{}".format(mode))
                logger.error("use big_cores instead")
                return 2

        config["power_mode"] = "big_cores"
        config["power_mode_id"] = power_mode_id(config["power_mode"])
        config["bench_cmd_pattern"] = (
            "adb -s {serial_num} shell {device_benchmark_bin} {model_dir}"
            " {repeats} {warmup} {thread_num} {power_mode} {gpu_device}"
        )
    else:
        logger.info("Unsupported framework_name: {}".format(framework_name))
        exit(1)
    return config


class TestGlobalConfig(unittest.TestCase):
    def setUp(self):
        logger.info(
            "{} {}".format(
                self.__class__.__name__, sys._getframe().f_code.co_name  # noqa
            )  # noqa
        )

    def tearDown(self):
        logger.info(
            "{} {}".format(
                self.__class__.__name__, sys._getframe().f_code.co_name  # noqa
            )  # noqa
        )

    def test_config(self):
        tnn_config = create_config("tnn")
        logger.info("tnn_config:\n{}".format(tnn_config))
        self.assertNotEqual(tnn_config, dict())


if __name__ == "__main__":
    unittest.main()

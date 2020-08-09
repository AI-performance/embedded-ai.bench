#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import unittest

sys.path.append("..")
from utils.log import LoggerCreator  # noqa

##############################
# Global Config
##############################
log_enable_debug = True
logger_creator = LoggerCreator(log_enable_debug)
logger = logger_creator.create_logger()
GPU_REPEATS = 1000  # 1000
CPU_REPEATS = 100  # 100
WARMUP = 20  # 20
MAX_TIMEOUT_SECOND = 10  # 10, not used for infer command
MAX_TIMEOUT_SECOND_ONCE_INFER = 0.5  # used to calc MAX_TIMEOUT_SECOND


def create_config(framework_name):
    benchmark_platform = ["android-armv7", "android-armv8"]
    config = dict()
    config["warmup"] = WARMUP
    #############################
    # TNN config
    #############################
    if framework_name == "tnn":
        # note(ysh329):
        # https://github.com/Tencent/TNN/blob/master/doc/cn/user/test.md
        config["work_dir"] = "./{}".format(framework_name)

        def backend_to_repeats(backend):
            if backend == "OPENCL":
                return GPU_REPEATS
            elif backend == "ARM":
                return CPU_REPEATS
            else:
                logger.fatal("Unsupported backend {}".format(backend))
                exit(1)

        config["repeats"] = backend_to_repeats
        config["engine_repo"] = "https://github.com/Tencent/TNN.git"
        config[
            "model_repo"
        ] = "https://github.com/ai-performance/{}-models.git".format(  # noqa
            framework_name  # noqa
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

        def support_backend_id(backend="ARM"):
            backend = str(backend)
            backend_dict = {
                "ARM": "ARM",
                "OPENCL": "GPU_OPENCL",
            }
            return backend_dict[backend]

        config["support_backend_id"] = support_backend_id
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
    #############################
    # NCNN config
    #############################
    elif framework_name == "ncnn":
        # note(ysh329):
        # https://github.com/Tencent/ncnn/tree/master/benchmark/README.md
        config["work_dir"] = "./{}".format(framework_name)

        def backend_to_repeats(backend):
            backend = str(backend)
            if "ARM" in backend or "-1" in backend:
                return CPU_REPEATS
            elif "GPU" in backend or "0" in backend:
                return GPU_REPEATS
            else:
                return CPU_REPEATS

        config["repeats"] = backend_to_repeats
        config["engine_repo"] = "https://github.com/Tencent/NCNN.git"
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
            ] = "./ncnn/build-android-{}-vulkan/benchmark/benchncnn".format(
                "armv7" if "v7" in platform else "aarch64"
            )
            config[platform]["shared_lib"] = "./ncnn/README.md"

        # gpu device: -1=cpu-only, 0=gpu0, 1=gpu1 ...
        def support_backend_id(backend="ARM"):
            backend = str(backend)
            backend_dict = {
                "-1": "ARM",
                "ARM": "-1",  # noqa
                "0": "GPU_VULKAN",
                "GPU_VULKAN": "0",
            }
            return backend_dict[backend]

        config["support_backend_id"] = support_backend_id
        config["support_backends"] = ["ARM", "GPU_VULKAN"]  # only used below
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
    #############################
    # MNN config
    #############################
    elif framework_name == "mnn":
        # note(ysh329): https://www.yuque.com/mnn/cn/tool_benchmark
        config["work_dir"] = "./{}".format(framework_name)

        # 0->CPU，1->Metal，3->OpenCL，6->OpenGL，7->Vulkan
        def backend_to_repeats(backend):
            backend = str(backend)
            if (
                backend == "GPU_OPENCL"
                or backend == "3"
                or backend == "GPU_OPENGL"
                or backend == "6"
                or backend == "GPU_VULKAN"
                or backend == "7"
            ):
                return GPU_REPEATS
            else:
                return CPU_REPEATS

        config["repeats"] = backend_to_repeats
        config["engine_repo"] = "https://github.com/alibaba/MNN.git"
        config[
            "model_repo"
        ] = "https://github.com/ai-performance/{}-models.git".format(  # noqa
            framework_name  # noqa
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
            shared_libs = [
                "libMNN.so",
                "libMNN_CL.so",
                "libMNN_GL.so",
                "libMNN_Vulkan.so",
                "libMNN_Express.so",
            ]  # noqa
            shared_libs = map(
                lambda so_lib: "./mnn/benchmark/build_{}/{}".format(
                    32 if "v7" in platform else 64, so_lib
                ),
                shared_libs,
            )
            shared_libs = list(shared_libs)
            config[platform]["shared_lib"] = shared_libs
            config[platform][
                "benchmark_bin"
            ] = "./mnn/benchmark/build_{}/benchmark.out".format(
                32 if "v7" in platform else 64
            )

        # 0->CPU，1->Metal，3->OpenCL，6->OpenGL，7->Vulkan
        def support_backend_id(backend="0"):
            backend_dict = {
                "0": "ARM",
                "ARM": "0",
                "3": "GPU_OPENCL",
                "GPU_OPENCL": "3",
                "6": "GPU_OPENGL",
                "GPU_OPENGL": "6",
                "7": "GPU_VULKAN",
                "GPU_VULKAN": "7",
            }
            return backend_dict[backend]

        config["support_backend_id"] = support_backend_id
        # 0->CPU，1->Metal，3->OpenCL，6->OpenGL，7->Vulkan
        config["support_backend"] = ["0", "3", "6", "7"]
        config["is_cpu_backend"] = (
            lambda b: str(b).upper() == "ARM" or str(b).upper() == "0"
        )  # noqa
        config["cpu_thread_num"] = [1, 2, 4]
        # power_mode: "big_cores" # "little_cores", "no_bind"
        config["power_mode"] = "big_cores"  # default is big_cores
        config["bench_cmd_pattern"] = (
            "adb -s {serial_num} shell "
            '"export LD_LIBRARY_PATH={device_work_dir};'
            "{device_benchmark_bin} {model_dir} {repeats} {warmup} "
            '{forwardtype} {thread_num}"'  # {precision}"'
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
        framework_list = ["tnn", "mnn", "ncnn"]
        for fidx in range(len(framework_list)):
            framework = framework_list[fidx]
            framework_config = create_config(framework)
            logger.info("{}_config:\n{}".format(framework, framework_config))
            self.assertNotEqual(framework_config, dict())


if __name__ == "__main__":
    unittest.main()

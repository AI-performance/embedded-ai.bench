#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import time
import unittest

sys.path.append("..")  # noqa
from core.global_config import logger  # noqa
from utils.device import (  # noqa
    get_adb_devices,
    get_target_freq_idx,
    get_cpu_max_freqs,
    get_battery_level,
    get_system_version,
    get_imei,
)  # noqa
from utils.cmd import run_cmds, run_cmd  # noqa
from utils.misc import pattern_match, get_file_name  # noqa


class Engine:
    def __init__(self, config_dict):
        self.root_dir = os.getcwd()
        os.chdir(config_dict["work_dir"])
        self.config = config_dict
        self.prepare_engine()

    def __del__(self):
        os.chdir(self.root_dir)

    def engine_name(self):
        return self.config["framework_name"]

    def set_config(self, key, value):
        self.config[key] = value
        return self.config

    def prepare_engine(self):
        logger.info("==== {} ====".format(self.prepare_engine.__name__))
        lookup_branch_name_cmd = "cd {}; git branch".format(
            self.config["framework_name"]
        )
        branch = run_cmd(lookup_branch_name_cmd)[0].replace("* ", "")
        self.config["framework_repo_branch"] = branch
        logger.info(
            "framework_repo_branch:{}".format(
                self.config["framework_repo_branch"]  # noqa
            )  # noqa
        )
        lookup_commit_id_cmd = "cd {}; git rev-parse --short HEAD".format(
            self.config["framework_name"]
        )
        commit_id = run_cmd(lookup_commit_id_cmd)[0]
        self.config["framework_repo_commit_id"] = commit_id
        logger.info(
            "framework_repo_commit_id:{}".format(
                self.config["framework_repo_commit_id"]
            )
        )

    def prepare_models(self):
        logger.info("==== {} ====".format(self.prepare_models.__name__))
        cmds = list()
        framework_name = self.config["framework_name"]
        model_repo = self.config["model_repo"]
        model_type_keyword = self.config["model_type_keyword"]
        repo_name = get_file_name(model_repo, False)
        logger.info("repo_name:{}".format(repo_name))
        logger.debug("os.path.exists:{}".format(os.path.exists(repo_name)))
        if os.path.exists(repo_name):
            clone_models_cmd = "ls {}".format(repo_name)
        else:
            clone_models_cmd = "git clone {}".format(model_repo)
        model_repo_version_cmd = (
            'cd ./{}-models/; git log --pretty=format:"SHA-1:%h date:%ad" '
            '--date=format:"%y-%m-%d" -n1 #--shortstat -n1'.format(
                framework_name
            )  # noqa
        )
        model_repo_version_extra_cmd = (
            "cd ./{}-models/; "
            'git log --pretty=format:"SHA-1:%h - author:%an date:%ad '
            'note:%s" --date=format:"%y-%m-%d %H:%M:%S" -n1'.format(
                framework_name
            )  # noqa
        )
        model_repo_branch_cmd = "cd ./{}-models/; git branch | sed 's/\* //g'".format(  # noqa
            framework_name
        )
        lookup_models_path_cmd = "realpath ./{}-models/*{}*".format(
            framework_name, model_type_keyword
        )

        cmds.extend(
            [
                clone_models_cmd,
                model_repo_version_cmd,
                model_repo_version_extra_cmd,
                model_repo_branch_cmd,
                lookup_models_path_cmd,
            ]
        )

        cmds_res = run_cmds(cmds)

        # TODO(ysh329): add model_repo_version to config
        # self.config["model_repo_branch"] =
        # cmds_res[model_repo_branch_cmd][0]
        # self.config["model_repo_version"] =
        # cmds_res[model_repo_version_cmd].readalines()[0]
        # self.config["model_repo_version_extra"] =
        # cmds_res[model_repo_version_extra_cmd].readalines()[0]

        models_dir = list(
            map(lambda path: path.strip(), cmds_res[lookup_models_path_cmd])  # noqa
        )

        model_dict = dict()
        for midx in range(len(models_dir)):
            model_dir = models_dir[midx]
            logger.debug("{} {}".format(midx, model_dir))
            file_type = model_dir.split(".")[-1]
            model_name = (
                model_dir.split("/")[-1]
                .replace("." + file_type, "")
                .replace(file_type, "")
            )
            logger.debug(
                "model_name:{}, file_type:{}".format(model_name, file_type)
            )  # noqa
            model_dict[model_name] = model_dir
        logger.debug(models_dir)
        logger.debug(model_dict)
        return model_dict

    def prepare_devices(self):
        logger.info("==== {} ====".format(self.prepare_devices.__name__))

        device_status_dict = get_adb_devices(True)
        serial_num_list = list(device_status_dict.keys())
        logger.debug(serial_num_list)

        device_dict = dict()
        for sidx in range(len(serial_num_list)):
            device_serial_num = serial_num_list[sidx]
            device_status = device_status_dict[device_serial_num]
            if device_status != "device":
                logger.info(
                    "device {} status is {}, skipped".format(
                        device_serial_num, device_status
                    )
                )
                continue
            device_dict[device_serial_num] = dict()
            device_dict[device_serial_num]["status"] = device_status
            device_dict[device_serial_num]["cpu_max_freqs"] = get_cpu_max_freqs(  # noqa
                device_serial_num
            )
            cpu_max_freqs = get_cpu_max_freqs(device_serial_num)
            cpu_valid_freqs = list(
                filter(lambda freq: freq is not None, cpu_max_freqs)
            )  # noqa
            big_cores_idx = get_target_freq_idx(
                max(cpu_valid_freqs), device_serial_num, cpu_max_freqs
            )
            big_cores_idx_str = ",".join(big_cores_idx)
            little_cores_idx = get_target_freq_idx(
                min(cpu_valid_freqs), device_serial_num, cpu_max_freqs
            )
            little_cores_idx_str = ",".join(little_cores_idx)
            device_dict[device_serial_num]["big_cores_idx"] = big_cores_idx_str
            device_dict[device_serial_num][
                "little_cores_idx"
            ] = little_cores_idx_str  # noqa
            if self.config["power_mode"] == "big_cores":
                device_dict[device_serial_num][
                    "bind_cpu_idx"
                ] = big_cores_idx_str  # noqa
            elif self.config["power_mode"] == "little_cores":
                device_dict[device_serial_num][
                    "bind_cpu_idx"
                ] = little_cores_idx_str  # noqa
            elif self.config["power_mode"] == "no_bind":
                device_dict[device_serial_num]["bind_cpu_idx"] = ",".join(
                    map(str, range(len(cpu_max_freqs)))
                )
            else:
                logger.info(
                    "Unsupported power_mode:{}".format(
                        self.config["power_mode"]
                    )  # noqa
                )
                exit(1)

            # battery level
            device_dict[device_serial_num]["battery_level"] = get_battery_level(  # noqa
                device_serial_num
            )

            # system version
            device_dict[device_serial_num][
                "system_version"
            ] = get_system_version(  # noqa
                device_serial_num
            )

            # imie
            device_dict[device_serial_num]["imei"] = get_imei(device_serial_num)  # noqa

            # ro.board.platform, ro.board.chiptype, ro.board.hardware
            device_soc_cmd = (
                "adb -s {} shell getprop |"
                " grep 'ro.board.platform'".format(device_serial_num)
            )
            cmd_handls = run_cmds([device_soc_cmd])
            soc = cmd_handls[device_soc_cmd][0]
            soc = soc.split(": ")[1].strip().replace("[", "").replace("]", "")  # noqa
            device_dict[device_serial_num]["soc"] = soc
            logger.debug(soc)

            # product
            device_product_cmd = (
                "adb -s {} shell getprop | "
                "grep 'ro.product.model'".format(device_serial_num)
            )
            cmd_handle = run_cmd(device_product_cmd)
            product = cmd_handle[0]
            product = (
                product.split(": ")[1].strip().replace("[", "").replace("]", "")  # noqa
            )  # noqa
            device_dict[device_serial_num]["product"] = product
            logger.debug(product)

        logger.debug(device_dict)
        logger.info("len(device_dict):{}".format(len(device_dict)))
        return device_dict

    def prepare_models_for_devices(self):
        logger.info(
            "==== {} ====".format(self.prepare_models_for_devices.__name__)
        )  # noqa
        device_work_dir = self.config["device_work_dir"]
        device_dict = self.config["device_dict"]
        model_dict = self.config["model_dict"]

        device_serials = list(device_dict.keys())
        model_names = list(model_dict.keys())
        logger.debug(model_dict)

        cmds = list()
        for didx in range(len(device_serials)):
            device_serial = device_serials[didx]
            mkdir_cmd = "adb -s {} shell mkdir -p {}".format(
                device_serial, device_work_dir
            )
            cmds.append(mkdir_cmd)
            for midx in range(len(model_names)):
                model_name = model_names[midx]
                model_proto = model_dict[model_name]

                if (
                    self.config["framework_name"] == "ncnn"
                    or self.config["framework_name"] == "tnn"
                ):
                    model_param = model_proto.replace("tnnproto", "tnnmodel")
                elif self.config["framework_name"] == "mnn":
                    model_param = None
                else:
                    logger.fatal(
                        "Unsupported framework {}".format(  # noqa
                            self.config["framework_name"]  # noqa
                        )  # noqa
                    )
                    exit(1)

                push_proto_cmd = "adb -s {} push {} {}".format(
                    device_serial,
                    model_proto,
                    "/".join([device_work_dir, os.path.basename(model_proto)]),  # noqa
                )
                push_param_cmd = "adb -s {} push {} {}".format(
                    device_serial, model_param, device_work_dir
                )
                push_param_cmd = (
                    "echo" if model_param is None else push_param_cmd
                )  # noqa
                cmds.extend([push_proto_cmd, push_param_cmd])

        run_cmds(cmds)
        return 0

    # assets: benchmark_bin, benchmark_lib
    def prepare_benchmark_assets_for_devices(self):
        logger.info(
            "==== {} ====".format(
                self.prepare_benchmark_assets_for_devices.__name__
            )  # noqa
        )
        benchmark_platform = self.config["benchmark_platform"]
        device_work_dir = self.config["device_work_dir"]
        device_dict = self.config["device_dict"]
        device_serials = list(device_dict.keys())

        cmds = list()
        for didx in range(len(device_serials)):
            device_serial = device_serials[didx]
            for pidx in range(len(benchmark_platform)):
                platform = benchmark_platform[pidx]
                device_work_dir_platform = device_work_dir + "/" + platform
                # benchmark assets
                benchmark_bin = self.config[platform]["benchmark_bin"]
                benchmark_lib = self.config[platform]["shared_lib"]
                benchmark_libs = (
                    benchmark_lib
                    if isinstance(benchmark_lib, list)
                    else [benchmark_lib]
                )

                # create cmds
                rmdir_cmd = "adb -s {} shell rm -rf {}".format(
                    device_serial, device_work_dir_platform
                )
                mkdir_cmd = "adb -s {} shell mkdir -p {}".format(
                    device_serial, device_work_dir_platform
                )

                # lib
                benchmark_lib_device_paths = map(
                    lambda lib: device_work_dir_platform
                    + "/"
                    + os.path.basename(lib),  # noqa
                    benchmark_libs,
                )
                benchmark_lib_device_paths = list(benchmark_lib_device_paths)
                logger.debug(
                    "benchmark_lib_device_paths:{}".format(  # noqa
                        benchmark_lib_device_paths  # noqa
                    )  # noqa
                )
                push_shared_lib_cmds = map(
                    lambda lib, lib_device: "adb -s {} push {} {}".format(  # noqa
                        device_serial, lib, lib_device
                    ),
                    benchmark_libs,
                    benchmark_lib_device_paths,
                )
                push_shared_lib_cmds = list(push_shared_lib_cmds)
                push_shared_lib_cmds = (
                    ["echo"] if benchmark_lib is None else push_shared_lib_cmds
                )
                logger.debug(
                    "push_shared_lib_cmds:{}".format(  # noqa
                        push_shared_lib_cmds
                    )  # noqa
                )
                logger.debug(
                    "len(push_shared_lib_cmds):{}".format(  # noqa
                        len(push_shared_lib_cmds)  # noqa
                    )  # noqa
                )

                # bin
                benchmark_bin_device_path = (
                    device_work_dir_platform
                    + "/"
                    + os.path.basename(benchmark_bin)  # noqa
                )
                push_benchmark_bin_cmd = "adb -s {} push {} {}".format(
                    device_serial, benchmark_bin, benchmark_bin_device_path
                )
                chmod_x_bin_cmd = "adb -s {} shell chmod +x {}".format(
                    device_serial, benchmark_bin_device_path
                )

                cmds.extend([rmdir_cmd, mkdir_cmd])
                cmds.extend(push_shared_lib_cmds)
                cmds.extend([push_benchmark_bin_cmd, chmod_x_bin_cmd])
        logger.info(cmds)
        run_cmds(cmds)
        return 0

    def run_bench(self):
        logger.info("==== {} ====".format(self.run_bench.__name__))
        device_work_dir = self.config["device_work_dir"]
        device_dict = self.config["device_dict"]
        model_dict = self.config["model_dict"]

        device_serials = list(device_dict.keys())
        model_names = list(model_dict.keys())

        benchmark_platform = self.config["benchmark_platform"]
        support_backend = self.config["support_backend"]
        bench_cmd_pattern = self.config["bench_cmd_pattern"]
        bench_dict = dict()
        bench_case_idx = 0
        for didx in range(len(device_serials)):
            device_serial_num = device_serials[didx]
            logger.debug(
                "didx:{}, serial_num:{}".format(didx, device_serial_num)  # noqa
            )
            bench_dict[device_serial_num] = dict()
            for pidx in range(len(benchmark_platform)):
                platform = benchmark_platform[pidx]
                device_work_dir_platform = device_work_dir + "/" + platform  # noqa
                device_benchmark_bin = "/".join(
                    [
                        device_work_dir_platform,
                        os.path.basename(
                            self.config[platform]["benchmark_bin"]
                        ),  # noqa
                    ]
                )
                bench_dict[device_serial_num][platform] = dict()
                logger.debug("pidx:{}, platform:{}".format(pidx, platform))
                for midx in range(len(model_names)):
                    model_name = model_names[midx]
                    model_dir = "/".join(
                        [
                            device_work_dir,
                            os.path.basename(model_dict[model_name]),
                        ]  # noqa
                    )
                    logger.debug(
                        "midx:{}, model_name:{}, model_dir:{}".format(
                            midx, model_name, model_dir
                        )
                    )
                    bench_dict[device_serial_num][platform][model_name] = dict()  # noqa
                    for bidx in range(len(support_backend)):
                        backend = support_backend[bidx]
                        is_cpu = self.config["is_cpu_backend"]
                        logger.debug(
                            "bidx:{}, backend:{}".format(bidx, backend)
                        )  # noqa
                        bench_dict[device_serial_num][platform][model_name][
                            backend
                        ] = dict()  # noqa
                        for tidx in range(
                            len(self.config["cpu_thread_num"])
                            if is_cpu(backend)
                            else 1  # noqa
                        ):
                            bench_case_idx += 1
                            logger.info(
                                "\n\nbench_case_idx(from 1):{}".format(
                                    bench_case_idx
                                )  # noqa
                            )
                            cpu_thread_num = self.config["cpu_thread_num"][tidx]  # noqa
                            bench_dict[device_serial_num][platform][model_name][  # noqa
                                backend
                            ][
                                cpu_thread_num
                            ] = dict()  # noqa
                            #######################
                            # bench start
                            #######################
                            if self.config["framework_name"] == "tnn":
                                bench_cmd = bench_cmd_pattern.format(
                                    **{
                                        "serial_num": device_serial_num,
                                        "device_work_dir": device_work_dir_platform,  # noqa
                                        "device_benchmark_bin": device_benchmark_bin,  # noqa
                                        "model_type": self.config[
                                            "framework_name"
                                        ],  # noqa
                                        "model_dir": model_dir,
                                        "backend": backend,
                                        "repeats": self.config["repeats"](
                                            backend
                                        ),  # noqa
                                        "warmup": self.config["warmup"],
                                        "thread_num": cpu_thread_num,
                                        "bind_cpu_idx": device_dict[
                                            device_serial_num
                                        ][  # noqa
                                            "bind_cpu_idx"
                                        ],
                                    }
                                )
                            elif self.config["framework_name"] == "ncnn":
                                bench_cmd = bench_cmd_pattern.format(
                                    **{
                                        "serial_num": device_serial_num,
                                        "device_benchmark_bin": device_benchmark_bin,  # noqa
                                        "model_dir": model_dir,
                                        "repeats": self.config["repeats"](
                                            backend
                                        ),  # noqa
                                        "warmup": self.config["warmup"],
                                        "thread_num": cpu_thread_num,
                                        "power_mode": self.config[
                                            "power_mode_id"
                                        ],  # noqa
                                        "gpu_device": backend,
                                    }
                                )
                            elif self.config["framework_name"] == "mnn":
                                # '{device_benchmark_bin} {model_dir} {repeats} {warmup}'  # noqa
                                # '{forwardtype} {thread_num} {precision}"'
                                bench_cmd = bench_cmd_pattern.format(
                                    **{
                                        "serial_num": device_serial_num,
                                        "device_work_dir": device_work_dir_platform,  # noqa
                                        "device_benchmark_bin": device_benchmark_bin,  # noqa
                                        "model_dir": model_dir,
                                        "repeats": self.config["repeats"](
                                            backend
                                        ),  # noqa
                                        "warmup": self.config["warmup"],
                                        "thread_num": cpu_thread_num,
                                        "forwardtype": backend,
                                        # power_mode: big_core default
                                    }
                                )
                            else:
                                logger.fatal(
                                    "Unsupported framework {}".format(
                                        self.config["framework_name"]
                                    )
                                )
                                exit(1)

                            cmd_res = run_cmd(
                                bench_cmd, wait_interval_sec=3  # noqa
                            )  # noqa
                            perf_dict = self.parse_benchmark(cmd_res)
                            #################################
                            # summarize benchmark info
                            #################################
                            bench_record = {
                                "soc": device_dict[device_serial_num]["soc"],
                                "product": device_dict[device_serial_num][  # noqa
                                    "product"
                                ],  # noqa
                                "serial_num": device_serial_num,
                                "platform": platform,
                                "model_name": model_name,
                                "repeats": self.config["repeats"](backend),
                                "warmup": self.config["warmup"],
                                "avg": perf_dict["avg"],
                                "max": perf_dict["max"],
                                "min": perf_dict["min"],
                                "std_dev": perf_dict["std_dev"],
                                "backend": backend,
                                "cpu_thread_num": cpu_thread_num,
                                "power_mode": self.config["power_mode"],
                                "bind_cpu_idx": device_dict[device_serial_num][
                                    "bind_cpu_idx"
                                ],
                                "cpu_max_freqs": device_dict[device_serial_num][  # noqa
                                    "cpu_max_freqs"
                                ],
                                "battery_level": device_dict[device_serial_num][  # noqa
                                    "battery_level"
                                ],
                                "system_version": device_dict[
                                    device_serial_num
                                ][  # noqa
                                    "system_version"
                                ],
                                "cmd": bench_cmd,
                                "imei": device_dict[device_serial_num]["imei"],
                            }
                            bench_dict[device_serial_num][platform][model_name][  # noqa
                                backend
                            ][
                                cpu_thread_num
                            ] = bench_record  # noqa
                            # bench_dict[model_name].append(bench_record)
                            logger.info(bench_record)
        return bench_dict

    def parse_benchmark(self, cmd_res):
        logger.info("==== {} ====".format(self.parse_benchmark.__name__))
        output_lines = cmd_res
        logger.debug(output_lines)
        framework_name = self.config["framework_name"]
        benchmark = dict()
        if framework_name == "tnn" or framework_name == "mnn":
            if framework_name == "tnn":
                bench_res_keyword = "time cost"
            elif framework_name == "mnn":
                bench_res_keyword = "max ="
            output_lines = filter(  # noqa
                lambda line: bench_res_keyword in line, output_lines
            )
            output_lines = list(output_lines)
            assert len(output_lines) == 1
            line = output_lines[0].split()
            logger.debug(line)
            line = "".join(line)
            logger.debug(line)
            benchmark["min"] = pattern_match(line, "min=", "ms", False)
            benchmark["max"] = pattern_match(line, "max=", "ms", False)
            benchmark["avg"] = pattern_match(line, "avg=", "ms", False)
            benchmark["std_dev"] = pattern_match(line, "std_dev=", "ms", False)
        elif framework_name == "ncnn":
            is_no_vulkan = list(
                filter(lambda line: "no vulkan device" in line, output_lines)
            )
            is_no_vulkan = len(is_no_vulkan) > 0
            if is_no_vulkan:
                benchmark["min"] = 0.0
                benchmark["max"] = 0.0
                benchmark["avg"] = 0.0
                benchmark["std_dev"] = 0.0
            else:
                output_lines = filter(
                    lambda line: "min = " in line, output_lines
                )  # noqa
                output_lines = list(output_lines)
                logger.debug("output_lines:\n{}".format(output_lines))
                assert len(output_lines) == 1
                line = output_lines[0]
                line = line.split()
                logger.debug(line)
                line = "".join(line) + "END"
                benchmark["min"] = pattern_match(line, "min=", "max", False)
                benchmark["max"] = pattern_match(line, "max=", "avg", False)
                benchmark["avg"] = pattern_match(line, "avg=", "std_dev", False)  # noqa
                benchmark["std_dev"] = pattern_match(
                    line, "std_dev=", "END", False
                )  # noqa
        else:
            logger.fatal(
                "Unsupported framework {}".format(  # noqa
                    self.config["framework_name"]  # noqa
                )  # noqa
            )
            exit(1)
        logger.info("benchmark:{}".format(benchmark))
        assert len(benchmark) != 0
        return benchmark

    def generate_benchmark_summary(self, bench_dict, is_print_summary=True):
        logger.info(
            "==== {} ====".format(self.generate_benchmark_summary.__name__)
        )  # noqa
        summary_header = [
            "framework",
            "branch",
            "commit_id",
            "model_name",
            "platform",
            "soc",
            "product",
            "power_mode",
            "backend",
            "cpu_thread_num",
            "avg",
            "max",
            "min",
            "std_dev",
            "battery_level",
            "system_version",
            "repeats",
            "warmup",
            "imei",
        ]
        summary_header_str = ",".join(summary_header)
        summary = [summary_header_str]

        # bench_dict[device_serial_num][platform][model_name][support_backend][cpu_thread_num] = bench_record  # noqa
        device_serials = list(bench_dict.keys())
        for didx in range(len(device_serials)):
            serial = device_serials[didx]
            platforms = list(bench_dict[serial].keys())
            for pidx in range(len(platforms)):
                platform = platforms[pidx]
                model_names = list(bench_dict[serial][platform].keys())
                for midx in range(len(model_names)):
                    model_name = model_names[midx]
                    backends = list(
                        bench_dict[serial][platform][model_name].keys()
                    )  # noqa
                    for bidx in range(len(backends)):
                        backend = backends[bidx]
                        cpu_thread_nums = list(
                            bench_dict[serial][platform][model_name][
                                backend
                            ].keys()  # noqa
                        )  # noqa
                        for tidx in range(len(cpu_thread_nums)):
                            cpu_thread_num = cpu_thread_nums[tidx]
                            # get record
                            record_dict = bench_dict[serial][platform][
                                model_name
                            ][  # noqa
                                backend
                            ][
                                cpu_thread_num
                            ]  # noqa
                            record = [
                                self.config["framework_name"],
                                self.config["framework_repo_branch"],
                                self.config["framework_repo_commit_id"],
                                record_dict["model_name"],
                                record_dict["platform"],
                                record_dict["soc"],
                                record_dict["product"],
                                record_dict["power_mode"],
                                self.config["support_backend_id"](
                                    record_dict["backend"]
                                ),  # noqa
                                record_dict["cpu_thread_num"],
                                record_dict["avg"],
                                record_dict["max"],
                                record_dict["min"],
                                record_dict["std_dev"],
                                record_dict["battery_level"],
                                record_dict["system_version"],
                                record_dict["repeats"],
                                record_dict["warmup"],
                                record_dict["imei"],
                            ]
                            record_str = ",".join(map(str, record))
                            if True:
                                logger.info(record_str)
                            summary.append(record_str)
        if is_print_summary:
            summary_str = "\n".join(summary)
            logger.info("\n" + summary_str)
        return summary

    # TODO(ysh329): write summary with model verison, framework version
    def write_list_to_file(
        self, bench_list, out_file_dir=None, suffix=".bench.csv"
    ):  # noqa
        framework_name = self.config["framework_name"]
        if out_file_dir is None:
            time_stamp_human = time.strftime(
                "%Y%m%d-%H%M%S", time.localtime()  # noqa
            )  # noqa
            benchmark_platform = "".join(self.config["benchmark_platform"])
            framework_repo_branch = self.config["framework_repo_branch"]
            framework_repo_commit_id = self.config["framework_repo_commit_id"]
            model_version = str(1)  # noqa
            work_dir = self.config["work_dir"]  # noqa
            out_file_dir = "-".join(
                [
                    framework_name,
                    framework_repo_branch,
                    framework_repo_commit_id,
                    benchmark_platform,
                    time_stamp_human,
                ]
            )
            out_file_dir += suffix
            logger.info(
                "bench for {} 's out_file_dir:{}".format(  # noqa
                    framework_name, out_file_dir
                )  # noqa
            )

        bench_str = "\n".join(bench_list)
        with open(out_file_dir, "w") as f:
            f.writelines(bench_str)
            logger.info(
                "write {} benchmark result to {}".format(  # noqa
                    framework_name, out_file_dir
                )  # noqa
            )


class TestEngine(unittest.TestCase):
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

    """
    def test_tnn_engine(self):
        from core.global_config import create_config

        framework_name = "tnn"
        config_dict = create_config(framework_name)
        config_dict["work_dir"] = os.getcwd() + "/../tnn"

        tnn = Engine(config_dict)
        tnn.set_config("benchmark_platform", ["android-armv8"])
        tnn.set_config("support_backend", ["ARM"])
        tnn.set_config("cpu_thread_num", [2])
        tnn.config["repeats"] = lambda backend: 10 if backend == "ARM" else 20
        tnn.config["warmup"] = 2
        model_dict = tnn.prepare_models()
        device_dict = tnn.prepare_devices()
        if len(device_dict) == 0:
            logger.info("no device found")
            return 0
        config_dict = tnn.set_config("model_dict", model_dict)
        config_dict = tnn.set_config("device_dict", device_dict)

        tnn.prepare_models_for_devices()
        tnn.prepare_benchmark_assets_for_devices()

        bench_dict = tnn.run_bench()
        summary_list = tnn.generate_benchmark_summary(bench_dict)
        tnn.write_list_to_file(summary_list)
        summary_str = "\n".join(summary_list)
        logger.info("summary_str:\n{}".format(summary_str))
        return 0
    """

    """
    def test_ncnn_engine(self):
        from core.global_config import create_config

        framework_name = "ncnn"
        config_dict = create_config(framework_name)
        config_dict["work_dir"] = os.getcwd() + "/../ncnn"

        ncnn = Engine(config_dict)
        ncnn.set_config(
            "benchmark_platform", ["android-armv8", "android-armv7"]  # noqa
        )
        ncnn.set_config("support_backend", ["0"])  # -1: cpu, 0: gpu # noqa
        ncnn.set_config("cpu_thread_num", [1])  # 1, 2, 4
        ncnn.config["repeats"] = (
            lambda backend: 20 if backend == "VULKAN" else 10
        )  # noqa
        ncnn.config["warmup"] = 2
        model_dict = ncnn.prepare_models()

        device_dict = ncnn.prepare_devices()
        if len(device_dict) == 0:
            logger.error("no device found")
            return 0
        config_dict = ncnn.set_config("model_dict", model_dict)
        config_dict = ncnn.set_config("device_dict", device_dict)

        ncnn.prepare_models_for_devices()
        ncnn.prepare_benchmark_assets_for_devices()

        bench_dict = ncnn.run_bench()
        summary_list = ncnn.generate_benchmark_summary(bench_dict)
        ncnn.write_list_to_file(summary_list)

        summary_str = "\n".join(summary_list)
        logger.info("summary_str:\n{}".format(summary_str))
        return 0
    """

    # """
    def test_mnn_engine(self):
        from core.global_config import create_config

        framework_name = "mnn"
        config_dict = create_config(framework_name)
        config_dict["work_dir"] = os.getcwd() + "/../mnn"

        mnn = Engine(config_dict)
        mnn.set_config("benchmark_platform", ["android-armv8", "android-armv7"])  # noqa

        mnn.set_config(
            "support_backend", ["3", "6", "7"]
        )  # 0->CPU，1->Metal，3->OpenCL，6->OpenGL，7->Vulkan
        mnn.set_config("cpu_thread_num", [1, 2, 4])  # [1, 2, 4]
        mnn.config["warmup"] = 2
        model_dict = mnn.prepare_models()
        device_dict = mnn.prepare_devices()
        if len(device_dict) == 0:
            logger.error("no device found")
            return 0
        config_dict = mnn.set_config("model_dict", model_dict)
        config_dict = mnn.set_config("device_dict", device_dict)

        mnn.prepare_models_for_devices()
        mnn.prepare_benchmark_assets_for_devices()

        bench_dict = mnn.run_bench()
        summary_list = mnn.generate_benchmark_summary(bench_dict)
        summary_str = "\n".join(summary_list)
        logger.info("summary_str:\n{}".format(summary_str))
        mnn.write_list_to_file(summary_list)
        return 0

    # """


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import unittest

sys.path.append("..")
from core.global_config import logger  # noqa
from utils.cmd import run_cmd, run_cmds  # noqa


def get_adb_devices(is_print_status=False):
    device_dict = dict()
    adb_device_cmd = "adb devices"
    res = run_cmd(adb_device_cmd)
    devices = res[1:]
    devices = list(map(lambda devi: devi.split("\t"), devices))
    logger.info(devices)
    for didx in range(len(devices)):
        dev = devices[didx]
        if len(dev) == 2:  # sublist: (serial_num, status)
            serial_num = dev[0]
            status = dev[1].strip()
            device_dict[serial_num] = status
            if is_print_status:
                logger.info(
                    "device_idx:{}, serial_num:{}, status:{}".format(
                        didx, serial_num, status
                    )
                )
    return device_dict


def get_cpu_max_freqs(serial_num):
    check_cpu_num_cmd = "adb -s {} shell cat /proc/cpuinfo | grep processor".format(  # noqa
        serial_num
    )
    cmd_res = run_cmd(check_cpu_num_cmd)
    cpu_num = len(cmd_res)
    check_cpu_max_freq_cmd_pattern = (
        "adb -s {} shell cat "
        "/sys/devices/system/cpu/cpu{}/cpufreq/cpuinfo_max_freq"  # noqa
    )
    cmds = map(
        lambda cpu_idx: check_cpu_max_freq_cmd_pattern.format(  # noqa
            serial_num, cpu_idx
        ),
        range(cpu_num),
    )
    cmds = list(cmds)

    try:
        cmd_res_list = run_cmds(cmds)
        logger.info(cmd_res_list[cmds[0]])
        cpu_max_freqs = map(lambda cmd_key: cmd_res_list[cmd_key], cmds)
    except IndexError:
        logger.warn(
            "cat: /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq:"  # noqa
            " Permission denied"  # noqa
        )
        logger.warn("replacing scaling_max_freq with cpuinfo_max_freq")
        cmds = map(lambda c: c.replace("cpuinfo", "scaling"), cmds)

        cmd_res_list = run_cmds(cmds)
        # logger.warn(cmd_res_list[cmds[0]].strip())
        cpu_max_freqs = map(
            lambda cmd_key: cmd_res_list[cmd_key].strip(), cmds  # noqa
        )  # noqa
    cpu_max_freqs = list(cpu_max_freqs)
    cpu_max_freqs = cpu_max_freqs[:cpu_num]
    # get str from list
    cpu_max_freqs = list(map(lambda l: l[0], cpu_max_freqs))
    logger.debug(
        "cpu_max_freqs:{}, cpu_num:{}".format(cpu_max_freqs, cpu_num)  # noqa
    )  # noqa
    is_valid_freq = (
        lambda freq_str: True
        if "No such file or director" not in freq_str
        else False  # noqa
    )
    cpu_max_freqs_ghz = map(
        lambda freq: float(freq) / 1e6 if is_valid_freq(freq) else None,  # noqa
        cpu_max_freqs,  # noqa
    )
    logger.debug(cpu_max_freqs_ghz)
    cpu_max_freqs_ghz = list(cpu_max_freqs_ghz)
    return cpu_max_freqs_ghz


def get_target_freq_idx(target_freq, serial_num, cpu_max_freqs=None):
    target_freq_idx_list = []
    if cpu_max_freqs is None:
        cpu_max_freqs = get_cpu_max_freqs(serial_num)
    for idx, f in enumerate(cpu_max_freqs):
        if f == target_freq:
            target_freq_idx_list.append(str(idx))
    return target_freq_idx_list


def get_battery_level(serial_num):
    unset_battery_cmd = "adb -s {} shell dumpsys battery reset".format(  # noqa
        serial_num
    )
    lookup_battery_cmd = (
        "adb -s {} shell dumpsys battery"
        " | grep level"
        " | tr -cd 0-9".format(serial_num)
    )
    cmds = [unset_battery_cmd, lookup_battery_cmd]
    cmd_res_dict = run_cmds(cmds)
    battery_level = cmd_res_dict[lookup_battery_cmd][0]
    return battery_level


class TestDevice(unittest.TestCase):
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

    def test_main(self):
        device_dict = get_adb_devices(True)
        serials = device_dict.keys()
        serials = list(serials)
        for sidx in range(len(serials)):
            ser = serials[sidx]
            status = device_dict[ser]
            # for each cpu's max freq
            cpus_max_freq = get_cpu_max_freqs(ser)
            max_freq = max(cpus_max_freq)
            min_freq = min(cpus_max_freq)
            max_freq_cluster_idx = get_target_freq_idx(
                max_freq, ser, cpus_max_freq
            )  # noqa
            min_freq_cluster_idx = get_target_freq_idx(
                min_freq, ser, cpus_max_freq
            )  # noqa

            battery_level = get_battery_level(ser)

            logger.info("sidx:{}, ser:{}, status:{}".format(sidx, ser, status))
            logger.info("cpus_max_freq:{}".format(cpus_max_freq))
            logger.info("max_freq:{}".format(max_freq))
            logger.info("max_freq_cluster_idx:{}".format(max_freq_cluster_idx))
            logger.info("min_freq:{}".format(min_freq))
            logger.info("min_freq_cluster_idx:{}".format(min_freq_cluster_idx))
            logger.info("battery_level:{}".format(battery_level))


if __name__ == "__main__":
    unittest.main()

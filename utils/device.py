#!/usr/bin/python
# -*- coding: UTF-8 -*-

from utils.global_var import logger
from utils.cmd import run_cmd, run_cmds


def get_adb_devices(is_print_status=False):
    device_dict = dict()
    adb_device_cmd = "adb devices"
    h = run_cmd(adb_device_cmd)
    devices = h.readlines()[1:]
    devices = list(map(lambda dev: dev.split("\t"), devices))
    logger.info(devices)
    for didx in range(len(devices)):
        dev = devices[didx]
        if len(dev) == 2:  # sublist: (serial_num, status)
            serial_num = dev[0]
            status = dev[1].strip()
            device_dict[serial_num] = status
            if is_print_status:
                logger.info("device_idx:{}, serial_num:{}, status:{}".format(didx, serial_num, status))
    return device_dict


def get_cpu_max_freqs(serial_num):
    check_cpu_num_cmd = "adb -s {} shell cat /proc/cpuinfo | grep processor".format(serial_num)
    cmd_handle = run_cmd(check_cpu_num_cmd)
    cpu_num = len(cmd_handle.readlines())
    check_cpu_max_freq_cmd_pattern = "adb -s {} shell cat /sys/devices/system/cpu/cpu{}/cpufreq/cpuinfo_max_freq"
    cmds = map(lambda cpu_idx: check_cpu_max_freq_cmd_pattern.format(serial_num, cpu_idx), range(cpu_num))
    cmds = list(cmds)

    try:
        cmd_handles = run_cmds(cmds)
        # logger.info(cmd_handles[cmds[0]].readline())
        cpu_max_freqs = map(lambda cmd_key: cmd_handles[cmd_key].readline().strip(), cmds)
    except IndexError:
        logger.warn("cat: /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: Permission denied")
        logger.warn("replacing scaling_max_freq with cpuinfo_max_freq")
        cmds = map(lambda c: c.replace("cpuinfo", "scaling"), cmds)

        cmd_handles = run_cmds(cmds)
        # logger.warn(cmd_handles[cmds[0]].readline().strip())
        cpu_max_freqs = map(lambda cmd_key: cmd_handles[cmd_key].readline().strip(), cmds)
    cpu_max_freqs = list(cpu_max_freqs)
    cpu_max_freqs = cpu_max_freqs[:cpu_num]
    logger.debug("cpu_max_freqs:{}, cpu_num:{}".format(cpu_max_freqs, cpu_num))
    is_valid_freq = lambda freq_str: True if "No such file or director" not in freq_str else False
    cpu_max_freqs_ghz = map(lambda freq: float(freq) / 1e6 if is_valid_freq(freq) else None, cpu_max_freqs)
    logger.debug(cpu_max_freqs_ghz)
    cpu_max_freqs_ghz = list(cpu_max_freqs_ghz)
    return cpu_max_freqs_ghz


def get_some_freq_idx(freq, serial_num, cpu_max_freqs=None):
    some_freq_idx_list = []
    if cpu_max_freqs == None:
        cpu_max_freqs = get_cpu_max_freqs(serial_num)
    for idx, f in enumerate(cpu_max_freqs):
        if f == freq:
            some_freq_idx_list.append(str(idx))
    return some_freq_idx_list


def test_main():
    device_dict = get_adb_devices(True)
    serials = device_dict.keys()
    serials = list(serials)
    for sidx in range(len(serials)):
        ser = serials[sidx]
        status = device_dict[ser]
        cpus_max_freq = get_cpu_max_freqs(ser)  # for each cpu's max freq
        max_freq = max(cpus_max_freq)
        min_freq = min(cpus_max_freq)
        max_freq_cluster_idx = get_some_freq_idx(max_freq, ser, cpus_max_freq)
        min_freq_cluster_idx = get_some_freq_idx(min_freq, ser, cpus_max_freq)

        logger.info("sidx:{}, ser:{}, status:{}".format(sidx, ser, status))
        logger.info("cpus_max_freq:{}".format(cpus_max_freq))
        logger.info("max_freq:{}".format(max_freq))
        logger.info("max_freq_cluster_idx:{}".format(max_freq_cluster_idx))
        logger.info("min_freq:{}".format(min_freq))
        logger.info("min_freq_cluster_idx:{}".format(min_freq_cluster_idx))


if __name__ == "__main__":
    test_main()

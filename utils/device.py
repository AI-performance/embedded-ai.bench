#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import unittest

sys.path.append("..")
from core.global_config import logger  # noqa
from utils.cmd import run_cmd, run_cmds  # noqa
from utils.misc import pattern_match  # noqa


def get_soc_info_from_soc_code(soc_code):
    ###############################
    # summ.: http://www.mydrivers.com/zhuanti/tianti/01/index.html
    # snapdragon
    ###############################
    soc_dict = {  # noqa
        ###############################
        # snapdragon SoC  # noqa
        # https://www.qualcomm.com/products/mobile-processors
        ###############################
        "kona": {
            "name": "SD865",
            "cpu": "Kryo585:1xA77@2.84+3xA77@2.42+4XA55@1.8",
            "gpu": "Adreno-650",
            "npu/apu/xpu/dsp": "Hexagon-698",
        },  # noqa
        "msmnile": {
            "name": "SD855",
            "cpu": "Kyro485:1xA76@2.84+3xA76@2.42+4xA55@1.8",
            "gpu": "Adreno-640@585",
            "npu/apu/xpu/dsp": "Hexagon-690",
        },  # noqa
        "sdm845": {
            "name": "SD845",
            "cpu": "Kyro385:8x@2.8",
            "gpu": "Adreno-630@710",
            "npu/apu/xpu/dsp": "Hexagon-685",
        },  # noqa
        "msm8998": {
            "name": "SD835",
            "cpu": "Kryo285:4x@2.45+4x@1.9",
            "gpu": "Adreno-540@670/710",
            "npu/apu/xpu/dsp": "Hexagon-682",
        },  # noqa
        "msm8916": {
            "name": "SD410",
            "cpu": "4xA53@1.2",
            "gpu": "Adreno-306",
            "npu/apu/xpu/dsp": "HexagonDSP(QDSP6)",
        },  # noqa
        "msm8953": {
            "name": "SD625",
            "cpu": "8×A53@2.0",
            "gpu": "Adreno-506",
            "npu/apu/xpu/dsp": "Hexagon-546",
        },  # noqa
        ###############################
        # kirin SoC  # noqa
        # http://www.hisilicon.com/en/Products/ProductList/Kirin
        ###############################
        "kirin710": {
            "name": "kirin710",
            "cpu": "4×A73@2.2+4×A53@1.7",
            "gpu": "Mali-G51",
            "npu/apu/xpu/dsp": "None",
        },  # noqa
        "kirin820": {
            "name": "kirin820",
            "cpu": "1xA76@2.36+3xA76@2.22+4xA55@1.84",
            "gpu": "Mali-G57 MP6",
            "npu/apu/xpu/dsp": "D110@Lite",
        },  # noqa
        "kirin810": {
            "name": "kirin810",
            "cpu": "2×A76@2.27+6×A55@1.88",
            "gpu": "Mali-G52",
            "npu/apu/xpu/dsp": "D100@Lite",
        },  # noqa
        "kirin990": {
            "name": "kirin990",
            "cpu": "2xA76@2.86+2xA76@2.36+4xA55@1.95",
            "gpu": "Mali-G76 MP16",
            "npu/apu/xpu/dsp": "1xLite+1xTiny",
        },  # noqa
        "kirin985": {
            "name": "kirin985",
            "cpu": "1xA76@2.58+3xA76@2.4+4xA55@1.84",
            "gpu": "Mali-G77 MP8",
            "npu/apu/xpu/dsp": "1xD110@Lite+1xD100@Tiny",
        },  # noqa
        "kirin980": {
            "name": "kirin980",
            "cpu": "2xA76@2.6+2xA76@1.92+4xA55@1.8",
            "gpu": "Mali-G76 MP10",
            "npu/apu/xpu/dsp": "Dual NPU",
        },  # noqa
        "kirin970": {
            "name": "kirin970",
            "cpu": "4xA73+4xA53",
            "gpu": "Mali-G72 MP12",
            "npu/apu/xpu/dsp": "Dedicated NPU",
        },  # noqa
        "kirin960": {
            "name": "kirin960",
            "cpu": "4xA73@2.4+4xA53@1.8",
            "gpu": "Mali-G71 MP8",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin950": {
            "name": "kirin950",
            "cpu": "4xA72@2.3+4xA53@1.8",
            "gpu": "Mali-T880 MP4",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin930": {
            "name": "kirin930",
            "cpu": "4xA53@2.2+4xA53@1.5",
            "gpu": "Mali-628@680 MP4",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin920": {
            "name": "kirin920",
            "cpu": "4xA15@1.7+4xA7@1.3",
            "gpu": "Mali-T624@600 MP4",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin910": {
            "name": "kirin910",
            "cpu": "4xA9@1.6",
            "gpu": "Mali-450@533 MP4",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin650": {
            "name": "kirin650",
            "cpu": "4xA53@2.0+4xA53@1.7",
            "gpu": "Mali-T830@900",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        "kirin620": {
            "name": "kirin620",
            "cpu": "8xA53@1.2",
            "gpu": "Mali-450@500 MP4",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        ###############################
        # Samsung
        # https://www.samsung.com/semiconductor/minisite/exynos/products/all-processors/
        ###############################
        "exynos5": {
            "name": "exynos 7872",
            "cpu": "2xA73@2.0+4xA53@1.6",
            "gpu": "Mali-G71",
            "npu/apu/xpu/dsp": "",
        },  # noqa
        ###############################
        # MediaTek
        # https://www.samsung.com/semiconductor/minisite/exynos/products/all-processors/
        ###############################
        "mt6755": {
            "name": "Helio P10 MT6755/6755M",
            "cpu": "2xA53@1.8+6xA53",
            "gpu": "Mali-T860@700 MP2",
        },
    }
    cur_soc_dict = dict()
    if soc_code in soc_dict.keys():
        cur_soc_dict = soc_dict[soc_code]
    else:
        cur_soc_dict["name"] = soc_code
        cur_soc_dict["cpu"] = "TODO"
        cur_soc_dict["gpu"] = "TODO"
        cur_soc_dict["npu/apu/xpu/dsp"] = "TODO"
    cur_soc_dict["code"] = soc_code
    return cur_soc_dict


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


def get_system_version(serial_num):
    lookup_sys_ver_cmd = "adb -s {} shell getprop ro.build.version.release".format(  # noqa
        serial_num
    )
    sys_ver = run_cmd(lookup_sys_ver_cmd)[0]
    logger.debug("system_version:{}".format(sys_ver))
    return sys_ver


def get_soc_code(serial_num):
    lookup_soc_code_cmd = (
        "adb -s {} shell getprop | "  # noqa
        "grep 'ro.board.platform'".format(serial_num)  # noqa
    )
    soc_code = run_cmd(lookup_soc_code_cmd)[0]
    soc_code = soc_code.split(": ")[1].strip().replace("[", "").replace("]", "")  # noqa
    logger.debug(soc_code)
    return soc_code


def get_product(serial_num):
    lookup_product_cmd = "adb -s {} shell getprop | grep 'ro.product.model'".format(  # noqa
        serial_num  # noqa
    )  # noqa
    product = run_cmd(lookup_product_cmd)[0]
    product = product.split(": ")[1].strip().replace("[", "").replace("]", "")  # noqa
    logger.debug(product)
    return product


def get_imei(serial_num):
    lookup_imei_cmd = "adb -s {} shell service call iphonesubinfo 1".format(  # noqa
        serial_num
    )
    imei_list = run_cmd(lookup_imei_cmd)
    imei_list = list(filter(lambda l: "." in l, imei_list))
    assert 0 < len(imei_list)
    imei_list = list(
        map(lambda l: pattern_match(l, "'", "'", False), imei_list)
    )  # noqa
    logger.debug("imei_list:{}".format(imei_list))
    imei_list = map(lambda l: l.replace(".", ""), imei_list)
    imei = "".join(imei_list)
    imei = imei.replace(" ", "")
    logger.debug("imei:{}".format(imei))
    return imei


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
            cpus_max_freq = list(
                filter(lambda freq: freq is not None, cpus_max_freq)
            )  # noqa
            max_freq = max(cpus_max_freq)
            min_freq = min(cpus_max_freq)
            max_freq_cluster_idx = get_target_freq_idx(
                max_freq, ser, cpus_max_freq
            )  # noqa
            min_freq_cluster_idx = get_target_freq_idx(
                min_freq, ser, cpus_max_freq
            )  # noqa

            battery_level = get_battery_level(ser)
            system_version = get_system_version(ser)
            imei = get_imei(ser)
            soc_code = get_soc_code(ser)
            product = get_product(ser)
            soc_dict = get_soc_info_from_soc_code(soc_code)

            logger.info("sidx:{}, ser:{}, status:{}".format(sidx, ser, status))
            logger.info("cpus_max_freq:{}".format(cpus_max_freq))
            logger.info("max_freq:{}".format(max_freq))
            logger.info("max_freq_cluster_idx:{}".format(max_freq_cluster_idx))
            logger.info("min_freq:{}".format(min_freq))
            logger.info("min_freq_cluster_idx:{}".format(min_freq_cluster_idx))
            logger.info("battery_level:{}".format(battery_level))
            logger.info("system_version:{}".format(system_version))
            logger.info("imei:{}".format(imei))
            logger.info("soc_code:{}".format(soc_code))
            logger.info("product:{}".format(product))
            logger.info("soc_dict:{}".format(soc_dict))


if __name__ == "__main__":
    unittest.main()

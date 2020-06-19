#!/usr/bin/python

from datetime import datetime
import time
import os
import re

DEBUG = False

def pattern_match(text, a, b, contain_a_b=False):
    reg_exp = r'%s(.*?)%s' % (a, b)
    if contain_a_b:
        reg_exp = r'(%s.*%s)' % (a, b)
    m = re.search(reg_exp, text)
    if m:
        return m.group(1)
    return ""


def get_cpu_max_freqs(serial_num):
    check_cpu_num_cmd = "adb -s {} shell cat /proc/cpuinfo | grep processor".format(serial_num)
    cmd_handle = run_cmd(check_cpu_num_cmd)
    cpu_num = len(cmd_handle.readlines())
    check_cpu_max_freq_cmd_pattern = "adb -s {} shell cat /sys/devices/system/cpu/cpu{}/cpufreq/cpuinfo_max_freq"
    cmds = map(lambda cpu_idx: check_cpu_max_freq_cmd_pattern.format(serial_num, cpu_idx), range(cpu_num))

    try:
        cmd_handles = run_cmds(cmds)
        #print(cmd_handles[cmds[0]].readline())
        cpu_max_freqs = map(lambda cmd_key: cmd_handles[cmd_key].readline().strip(), cmds)
    except IndexError:
        print("cat: /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: Permission denied")
        print("replacing scaling_max_freq with cpuinfo_max_freq")
        cmds = map(lambda c: c.replace("cpuinfo", "scaling"), cmds)

        cmd_handles = run_cmds(cmds)
        #print(cmd_handles[cmds[0]].readline().strip())
        cpu_max_freqs = map(lambda cmd_key: cmd_handles[cmd_key].readline().strip(), cmds)
    cpu_max_freqs = cpu_max_freqs[:cpu_num]
    if DEBUG: print(cpu_max_freqs)
    is_valid_freq = lambda freq_str: True if "No such file or director" not in freq_str else False
    cpu_max_freqs_ghz = map(lambda freq: float(freq) / 1e6 if is_valid_freq(freq) else None, cpu_max_freqs)
    if DEBUG: print(cpu_max_freqs_ghz)
    return cpu_max_freqs_ghz


def get_some_freq_idx(freq, serial_num):
    some_freq_idx_list = []
    cpu_max_freqs = get_cpu_max_freqs(serial_num)
    for idx, f in enumerate(cpu_max_freqs):
        if f == freq:
            some_freq_idx_list.append(str(idx))
    return some_freq_idx_list


# benchmark config
def create_config(framework_name):
    benchmark_platform = ["android-armv7", "android-armv8"]
    config = dict()
    if framework_name == "tnn":
        config['device_work_dir'] ="/data/local/tmp/ai-performance/{}".format(framework_name)
        config['framework_name'] = framework_name
        config['benchmark_platform'] = benchmark_platform
        for pidx in range(len(benchmark_platform)):
            platform = benchmark_platform[pidx]
            config[platform] = dict()
            config[platform]['shared_lib'] = "./tnn/scripts/build{}/libTNN.so".format(32 if "v7" in platform else 64)
            #config[platform]['benchmark_bin'] = "./tnn/scripts/build32/test/benchmark/TNNBench"
            config[platform]['benchmark_bin'] = "./tnn/scripts/build{}/test/TNNTest".format(32 if "v7" in platform else 64)
        config['repeats'] = 100
        config['warmup'] = 20
        config['support_backend'] = ["ARM", "OPENCL"]
        config["cpu_thread_num"] = [1, 2, 4]
        config["power_mode"] = "big_cores" #"big_cores" # "little_cores", "no_bind"
        config['benchmark_cmd_pattern'] = 'adb -s {serial_num} shell "export LD_LIBRARY_PATH={device_work_dir}; {device_benchmark_bin} -mt {model_type} -mp {model_dir} -dt {backend} -ic {repeats} -wc {warmup} -th {thread_num} -dl {bind_cpu_idx}"'
    else:
        print("Unsupported framework_name: {}".format(framework_name))
        exit(1)
    return config


def set_config(config, key, value):
    config[key] = value
    return config


def run_cmds(cmds, is_adb_cmd=False):
    cmd_handles = dict()
    for cidx in range(len(cmds)):
        cmd = cmds[cidx]
        current_time = datetime.now().ctime() + " " if DEBUG else ""
        cmd_type = "ADB CMD" if is_adb_cmd else "CMD"
        print("{}{}> {}".format(current_time, cmd_type, cmd))
        cmd_handles[cmd] = os.popen(cmd)
        # TODO(ysh329): wait shell finish, not a good method
        time.sleep(0.1)
    return cmd_handles


def run_cmd(cmd, bench_interval_second=0, cmd_type="CMD"):
    print("{}> {}".format(cmd_type, cmd))
    cmd_handle = os.popen(cmd)
    if bench_interval_second > 0:
        print("python> time.sleep({})".format(bench_interval_second))
        time.sleep(bench_interval_second)
    return cmd_handle


def prepare_models(config):
    print("=============== {} ===============".format(prepare_models.__name__))
    cmds = list()
    framework_name = config['framework_name']
    clone_models_cmd = "git clone https://gitee.com/yuens/{}-models.git".format(framework_name)
    lookup_models_path_cmd = "realpath ./{}-models/*{}*".format(framework_name, framework_name)
    cmds.extend([clone_models_cmd, lookup_models_path_cmd])

    cmd_handles = run_cmds(cmds)
    models_dir = map(lambda path: path.strip(), cmd_handles[lookup_models_path_cmd].readlines())

    model_dict = dict()
    for midx in range(len(models_dir)):
        if DEBUG: print("{} {}".format(midx, models_dir[midx]))
        model_dir = models_dir[midx]
        file_type = model_dir.split(".")[-1]
        model_name = model_dir.split("/")[-1].replace("." + file_type, "").replace(file_type, "")
        if DEBUG: print(model_name, file_type)
        if "proto" in model_dir: # filter proto files
            model_dict[model_name] = model_dir
    if DEBUG: print(models_dir)
    if DEBUG: print(model_dict)
    return model_dict


def prepare_devices(config):
    print("=============== {} ===============".format(prepare_devices.__name__))
    adb_devices_cmd = "adb devices"
    cmd_handles = run_cmds([adb_devices_cmd])
    serial_num_list = cmd_handles[adb_devices_cmd].readlines()[1:]
    serial_num_list = map(lambda device_line: device_line.strip(), serial_num_list)
    serial_num_list = serial_num_list[:len(serial_num_list)-1]
    if DEBUG: print(serial_num_list)

    device_dict = dict()
    for sidx in range(len(serial_num_list)):
        serial_num_line = serial_num_list[sidx]
        serial_num_line = serial_num_line.split("\t")
        device_serial_num = serial_num_line[0]
        device_status = serial_num_line[1].strip()
        if device_status != "device":
            print("device {} status is {}, skipped".format(device_serial_num, device_status))
            continue
        device_dict[device_serial_num] = dict()
        device_dict[device_serial_num]['status'] = device_status
        device_dict[device_serial_num]['cpu_max_freqs'] = get_cpu_max_freqs(device_serial_num)
        cpu_max_freqs = get_cpu_max_freqs(device_serial_num)
        cpu_valid_freqs = set(filter(lambda freq: freq != None, cpu_max_freqs))
        big_cores_idx = get_some_freq_idx(max(cpu_valid_freqs), device_serial_num)
        big_cores_idx_str = ",".join(big_cores_idx)
        little_cores_idx = get_some_freq_idx(min(cpu_valid_freqs), device_serial_num)
        little_cores_idx_str = ",".join(little_cores_idx)
        device_dict[device_serial_num]['big_cores_idx'] = big_cores_idx_str
        device_dict[device_serial_num]['little_cores_idx'] = little_cores_idx_str
        if config["power_mode"] == "big_cores":
            device_dict[device_serial_num]['bind_cpu_idx'] = big_cores_idx_str
        elif config["power_mode"] == "little_cores":
            device_dict[device_serial_num]['bind_cpu_idx'] = little_cores_idx_str
        elif config["power_mode"] == "no_bind":
            device_dict[device_serial_num]['bind_cpu_idx'] = ",".join(map(str, range(len(cpu_max_freqs))))
        else:
            print("Unsupported power_mode:{}".format(config["power_mode"]))
            exit(1)

        # ro.board.platform, ro.board.chiptype, ro.board.hardware
        device_soc_cmd = "adb -s {} shell getprop | grep 'ro.board.platform'".format(device_serial_num)
        cmd_handls = run_cmds([device_soc_cmd])
        soc = cmd_handls[device_soc_cmd].readlines()[0]
        soc = soc.split(": ")[1].strip().replace("[", "").replace("]", "")
        device_dict[device_serial_num]["soc"] = soc
        if DEBUG: print(soc)

        # product
        device_product_cmd = "adb -s {} shell getprop | grep 'ro.product.model'".format(device_serial_num)
        cmd_handle = run_cmd(device_product_cmd)
        product = cmd_handle.readlines()[0]
        product = product.split(": ")[1].strip().replace("[", "").replace("]", "")
        device_dict[device_serial_num]["product"] = product
        if DEBUG: print(product)

    if DEBUG: print(device_dict)
    assert(len(device_dict) > 0)
    return device_dict


def prepare_models_for_devices(config):
    print("=============== {} ===============".format(prepare_models_for_devices.__name__))
    device_work_dir = config['device_work_dir']
    device_dict = config['device_dict']
    model_dict = config['model_dict']

    device_serials = device_dict.keys()
    model_names = model_dict.keys()

    cmds = list()
    for didx in range(len(device_serials)):
        device_serial = device_serials[didx]
        mkdir_cmd = "adb -s {} shell mkdir -p {}".format(device_serial, device_work_dir)
        cmds.append(mkdir_cmd)
        for midx in range(len(model_names)):
            model_name = model_names[midx]
            model_proto = model_dict[model_name]
            model_param = model_proto.replace("tnnproto", "tnnmodel")
            push_proto_cmd = "adb -s {} push {} {}".format(device_serial, model_proto, device_work_dir)
            push_param_cmd = "adb -s {} push {} {}".format(device_serial, model_param, device_work_dir)
            cmds.extend([push_proto_cmd, push_param_cmd])
            if DEBUG: print([push_proto_cmd, push_param_cmd])

    run_cmds(cmds)
    return 0


# assets: benchmark_bin, benchmark_lib
def prepare_benchmark_assets_for_devices(config):
    print("=============== {} ===============".format(prepare_benchmark_assets_for_devices.__name__))
    benchmark_platform = config['benchmark_platform']
    device_work_dir = config["device_work_dir"]
    model_dict = config["model_dict"]
    device_dict = config["device_dict"]
    device_serials = device_dict.keys()
    model_names = model_dict.keys()

    cmds = list()
    for didx in range(len(device_serials)):
        device_serial = device_serials[didx]
        for pidx in range(len(benchmark_platform)):
            platform = benchmark_platform[pidx]
            device_work_dir_platform = device_work_dir + "/" + platform
            # benchmark assets
            benchmark_bin = config[platform]['benchmark_bin']
            benchmark_lib = config[platform]['shared_lib']

            rmdir_cmd = "adb -s {} shell rm -rf {}".format(device_serial, device_work_dir_platform)
            mkdir_cmd = "adb -s {} shell mkdir -p {}".format(device_serial, device_work_dir_platform)
            benchmark_lib_device_path = device_work_dir_platform + "/" + os.path.basename(benchmark_lib)
            benchmark_bin_device_path = device_work_dir_platform + "/" + os.path.basename(benchmark_bin)

            push_shared_lib_cmd = "adb -s {} push {} {}".format(device_serial, benchmark_lib, benchmark_lib_device_path)
            push_benchmark_bin_cmd = "adb -s {} push {} {}".format(device_serial, benchmark_bin, benchmark_bin_device_path)
            chmod_x_bin_cmd = "adb -s {} shell chmod +x {}".format(device_serial, benchmark_bin_device_path)

            cmds.extend([rmdir_cmd, mkdir_cmd, push_shared_lib_cmd, push_benchmark_bin_cmd, chmod_x_bin_cmd])

    run_cmds(cmds)
    return 0


def benchmark(config):
    print("=============== {} ===============".format(benchmark.__name__))
    device_work_dir = config["device_work_dir"]
    device_dict = config["device_dict"]
    model_dict = config["model_dict"]

    warmup = config["warmup"]
    repeats = config["repeats"]

    device_serials = device_dict.keys()
    model_names = model_dict.keys()

    benchmark_platform = config["benchmark_platform"]
    support_backend = config["support_backend"]
    benchmark_cmd_pattern = config['benchmark_cmd_pattern']
    bench_dict = dict()
    bench_case_idx = 0
    for didx in range(len(device_serials)):
        device_serial_num = device_serials[didx]

        for midx in range(len(model_names)):
            model_name = model_names[midx]
            model_dir = "/".join([device_work_dir, os.path.basename(model_dict[model_name])])
            bench_dict[model_name] = []

            for pidx in range(len(benchmark_platform)):
                platform = benchmark_platform[pidx]
                device_work_dir_platform = device_work_dir + "/" + platform
                device_benchmark_bin = "/".join([device_work_dir_platform,
                                                 os.path.basename(config[platform]['benchmark_bin'])])

                for bidx in range(len(support_backend)):
                    backend = support_backend[bidx]
                    is_cpu = lambda b: b == "CPU" or b == "ARM"                  
                    for tidx in range(len(config['cpu_thread_num']) if is_cpu(backend) else 1):
                        bench_case_idx += 1
                        print("\nbench_case_idx(from 1):{}".format(bench_case_idx))
                        cpu_thread_num = config['cpu_thread_num'][tidx]
                        benchmark_cmd = benchmark_cmd_pattern.format(**{"serial_num": device_serial_num,
                                                                        "device_work_dir": device_work_dir_platform,
                                                                        "device_benchmark_bin": device_benchmark_bin,
                                                                        "model_type": config['framework_name'].upper(),
                                                                        "model_dir": model_dir,
                                                                        "backend": backend,
                                                                        "repeats": config['repeats'],
                                                                        "warmup": config['warmup'],
                                                                        "thread_num": cpu_thread_num,
                                                                        "bind_cpu_idx": device_dict[device_serial_num]['bind_cpu_idx']})
                        cmd_handle = run_cmd(benchmark_cmd, bench_interval_second=3)
                        perf_dict = parse_benchmark(cmd_handle)
                        # summarize benchmark info
                        bench_record = {"soc": device_dict[device_serial_num]['soc'],
                                        "product": device_dict[device_serial_num]['product'],
                                        "serial_num": device_serial_num,
                                        "platform": platform,
                                        "model_name": model_name,
                                        "repeats": config['repeats'],
                                        "warmup": config['warmup'],
                                        "avg": perf_dict["avg"],
                                        "max": perf_dict["max"],
                                        "min": perf_dict["min"],
                                        "backend": backend,
                                        "cpu_thread_num": cpu_thread_num,
                                        "power_mode": config["power_mode"],
                                        "bind_cpu_idx": device_dict[device_serial_num]["bind_cpu_idx"],
                                        "cpu_max_freqs": device_dict[device_serial_num]["cpu_max_freqs"],
                                        "cmd": benchmark_cmd}
                        bench_dict[model_name].append(bench_record)
                        print(bench_record)
    return bench_dict


def generate_benchmark_summary(bench_dict, is_print_summary=True):
    print("=============== {} ===============".format(generate_benchmark_summary.__name__))
    summary_header = ["model_name", "platform", "soc", "product", "power_mode", "backend", "cpu_thread_num", "avg", "max", "min", "repeats", "warmup"]
    summary_header_str = ",".join(summary_header)
    summary = [summary_header_str]

    model_names = bench_dict.keys()
    model_names.sort()
    for midx in range(len(model_names)):
        model_name = model_names[midx]
        bench_records = bench_dict[model_name]
        print("len(bench_dict[model_name]):{}".format(len(bench_dict[model_name])))
        for ridx in range(len(bench_records)):
            record_dict = bench_records[ridx]
            print(record_dict)
            record = [record_dict["model_name"],
                      record_dict["platform"],
                      record_dict["soc"],
                      record_dict["product"],
                      record_dict["power_mode"],
                      record_dict["backend"],
                      record_dict["cpu_thread_num"],
                      record_dict["avg"],
                      record_dict["max"],
                      record_dict["min"],
                      record_dict["repeats"],
                      record_dict["warmup"]]
            record_str = ",".join(map(str, record))
            if True: print(record_str)
            summary.append(record_str)

    if is_print_summary:
        summary_str = "\n".join(summary)
        print("\n" + summary_str)
    return summary

def benchmark_sum(bench_dict):
    pass


def parse_benchmark(cmd_handle):
    output_lines = cmd_handle.readlines()
    if DEBUG: print(output_lines)
    output_lines = filter(lambda line: "time cost" in line, output_lines)
    assert(len(output_lines) == 1)
    benchmark = dict()
    line = output_lines[0].split()
    if DEBUG: print(line)
    line = "".join(line)
    if DEBUG: print(line)
    benchmark["min"] = pattern_match(line, "min=", "ms", False)
    benchmark["max"] = pattern_match(line, "max=", "ms", False)
    benchmark["avg"] = pattern_match(line, "avg=", "ms", False)
    assert(len(benchmark) != 0)
    return benchmark


def main():
    # TODO(ysh329): add args for backend / threads / powermode / armeabi etc.

    config_dict = create_config("tnn")
    model_dict = prepare_models(config_dict)
    device_dict = prepare_devices(config_dict)
    config_dict = set_config(config_dict, "model_dict", model_dict)
    config_dict = set_config(config_dict, "device_dict", device_dict)

    prepare_models_for_devices(config_dict)
    prepare_benchmark_assets_for_devices(config_dict)

    bench_dict = benchmark(config_dict)
    summary_list = generate_benchmark_summary(bench_dict)
    return 0


if __name__ == "__main__":
    main()

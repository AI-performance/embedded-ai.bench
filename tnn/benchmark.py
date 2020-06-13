#!/usr/bin/python

from datetime import datetime
import os

DEBUG = False

def run_cmds(cmds, is_adb_cmd=False):
    cmd_handles = dict()
    for cidx in range(len(cmds)):
        cmd = cmds[cidx]
        current_time = datetime.now().ctime() + " " if DEBUG else ""
        cmd_type = "ADB CMD" if is_adb_cmd else "CMD"
        print("{}{}> {}".format(current_time, cmd_type, cmd))
        cmd_handles[cmd] = os.popen(cmd)
    return cmd_handles


def prepare_models():
    cmds = list()
    clone_models_cmd = "git clone https://gitee.com/yuens/tnn-models.git"
    cmds.append(clone_models_cmd)

    lookup_models_path_cmd = "realpath ./tnn-models/*tnn*"
    cmds.append(lookup_models_path_cmd)

    cmd_handles = run_cmds(cmds)

    models_dir = map(lambda path: path.strip(), cmd_handles[lookup_models_path_cmd].readlines())

    model_dict = dict()
    for midx in range(len(models_dir)):
        print("{} {}".format(midx, models_dir[midx]))
        model_dir = models_dir[midx]
        file_type = model_dir.split(".")[-1]
        model_name = model_dir.split("/")[-1].replace("." + file_type, "").replace(file_type, "")
        print(model_name, file_type)
        if "proto" in model_dir: # filter proto files
            model_dict[model_name] = model_dir
    if DEBUG: print(models_dir)
    if DEBUG: print model_dict
    return model_dict


def prepare_devices():
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
        device_status = serial_num_line[1]
        device_dict[device_serial_num] = dict()
        device_dict[device_serial_num]['status'] = device_status

        # ro.board.platform, ro.board.chiptype
        device_platform_cmd = "adb -s {} shell getprop | grep 'cpu_info_display'".format(device_serial_num)
        cmd_handls = run_cmds([device_platform_cmd])
        soc = cmd_handls[device_platform_cmd].readlines()[0].split(": ")[1].strip().replace("[", "").replace("]", "")
        device_dict[device_serial_num]["soc"] = soc

    if DEBUG: print(device_dict)
    return device_dict


def prepare_models_for_devices(model_dict, device_dict, device_work_dir="/data/local/tmp/ai-performance/"):
    device_work_dir = device_work_dir + "/tnn/"
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


def main():
    # TODO(ysh329): add args for backend / threads / powermode / armeabi etc.
    model_dict = prepare_models()
    device_dict = prepare_devices()
    prepare_models_for_devices(model_dict, device_dict)


if __name__ == "__main__":
    main()

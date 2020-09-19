#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import threading
from time import ctime
import unittest


sys.path.append("..")
from core.global_config import logger, MAX_TIMEOUT_SECOND  # noqa


class MyThread(threading.Thread):
    def __init__(
        self,
        func,
        func_args_tuple,
        device_serial,
        thread_idx=-1,
        thread_num=-1,
        framework_name="undef",
    ):
        threading.Thread.__init__(self)
        self.func = func
        self.args = func_args_tuple
        self.res = None  # placeholder
        self.device_serial = device_serial
        self.thread_idx = thread_idx
        self.framework_name = framework_name

        self.start_time = ""
        self.end_time = ""

    def run(self):  # called by start()
        self.start_time = ctime()
        logger.debug(
            "start {} on device {} at {}".format(
                self.thread_idx, self.device_serial, self.start_time
            )
        )
        self.res = self.func(*self.args)
        self.end_time = ctime()
        logger.debug(
            "end thread(from0) {} on device {} at {}".format(
                self.thread_idx, self.device_serial, self.end_time
            )
        )

    def get_framework_name(self):
        return self.framework_name

    def get_thread_idx(self):
        return self.thread_idx

    def get_device_serial(self):
        return self.device_serial

    def get_result(self):
        return self.res


# note(ysh329): used for test below
def run_bench_for_test(config, serial, thread_idx):
    bench_dict = dict()
    bench_dict[serial] = dict()
    logger.info("start thread_idx: {} at {}".format(thread_idx, ctime()))
    logger.info("do nothing")
    logger.info("end thread_idx: {} at {}".format(thread_idx, ctime()))

    models = config["model_names"]
    platforms = config["benchmark_platform"]
    backends = config["support_backend"]
    logger.info("models:{}".format(models))
    logger.info("platforms:{}".format(platforms))
    logger.info("backends:{}".format(backends))

    for pidx in range(len(platforms)):
        platform = platforms[pidx]
        bench_dict[serial][platform] = dict()
        for midx in range(len(models)):
            model = models[midx]
            bench_dict[serial][platform][model] = dict()
            for bidx in range(len(backends)):
                backend = backends[bidx]
                bench_dict[serial][platform][model][backend] = dict()
                threads = [1, 2, 4] if backend == "ARM" else [1]
                for tidx in range(len(threads)):
                    thread = threads[tidx]
                    bench_dict[serial][platform][model][backend][thread] = []
                    # create cmd
                    concats = map(str, [platform, model, backend, thread])
                    concat = "-".join(concats)
                    cmd = "adb -s {} shell echo '{}'".format(serial, concat)

                    from utils.cmd import run_cmd

                    bench_record = run_cmd(cmd)

                    bench_dict[serial][platform][model][backend][
                        thread
                    ] = bench_record  # noqa
                    logger.info(bench_record)
    return bench_dict


class TestThreads(unittest.TestCase):
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

    def test_threads(self):
        import sys

        sys.path.append("..")
        from utils.device import get_adb_devices

        config = dict()
        config["benchmark_platform"] = ["android-armv7", "android-armv8"]
        config["model_names"] = ["caffe_mobilenetv1", "caffe_mobilenetv2"]
        config["support_backend"] = ["ARM"]

        device_serials = list(map(lambda t: t, get_adb_devices()))
        logger.info(device_serials)
        device_threads = dict()
        for didx in range(len(device_serials)):
            thread_idx = didx
            ser = device_serials[didx]
            logger.info("didx(from1):{}/{}".format(didx, len(device_serials)))
            device_threads[ser] = MyThread(
                func=run_bench_for_test,
                func_args_tuple=(config, ser, thread_idx),
                device_serial=ser,
                thread_idx=thread_idx,
            )
        assert len(device_serials) == len(device_threads)

        for didx in range(len(device_threads)):
            ser = device_serials[didx]
            device_threads[ser].start()

        for didx in range(len(device_threads)):
            ser = device_serials[didx]
            device_threads[ser].join()

        bench_dict = dict()
        for didx in range(len(device_serials)):
            ser = device_serials[didx]
            t = device_threads[ser]
            t_bench_dict = t.get_result()
            bench_dict[ser] = t_bench_dict[ser]
        return bench_dict


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import sys
import unittest

sys.path.append("..")
from core.global_config import logger  # noqa


def run_cmds(cmds, is_adb_cmd=False):
    cmd_handles = dict()
    cmds = list(cmds)
    for cidx in range(len(cmds)):
        cmd = cmds[cidx]
        cmd_type = "ADB CMD" if is_adb_cmd else "CMD"
        logger.info("{}> {}".format(cmd_type, cmd))
        cmd_handles[cmd] = os.popen(cmd)
        # TODO(ysh329): wait shell finish, not a good method
        time.sleep(0.1)
    return cmd_handles


def run_cmd(cmd, bench_interval_second=0, cmd_type="CMD"):
    logger.info("{}> {}".format(cmd_type, cmd))
    cmd_handle = os.popen(cmd)
    if bench_interval_second > 0:
        logger.info("python> time.sleep({})".format(bench_interval_second))
        time.sleep(bench_interval_second)
    return cmd_handle


class TestCmd(unittest.TestCase):
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

    def test_run_cmds(self):
        # run_cmds
        cmds = ["ls", "ls -l", "adb devices"]
        cmd_handls = run_cmds(cmds)
        for cidx in range(len(cmds)):
            cmd = cmds[cidx]
            h = cmd_handls[cmd]
            logger.info("cmd_idx:{}, cmd:{}".format(cidx, cmd))
            logger.info(h.readlines())

    def test_run_cmd(self):
        cmds = ["ls", "pwd", "adb devices"]
        for cidx in range(len(cmds)):
            cmd = cmds[cidx]
            h = run_cmd(cmd)
            logger.info("cmd_idx:{}, cmd:{}".format(cidx, cmd))
            logger.info(h.readlines())


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import sys
import time
import subprocess
import unittest

sys.path.append("..")
from core.global_config import logger, MAX_TIMEOUT_SECOND  # noqa


def run_cmd(cmd, wait_interval_sec=5, max_timeout_sec=MAX_TIMEOUT_SECOND):
    cmd_type = "CMD"
    logger.info("{}> {}".format(cmd_type, cmd))
    subp = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    try:
        subp.wait(max_timeout_sec)
    except subprocess.TimeoutExpired:
        logger.error(
            "TimeoutExpired {} seconds: {}, let's kill this subprocess".format(
                max_timeout_sec, cmd
            )  # noqa
        )
        subp.kill()
        return None

    subp_status = -1
    duration_sec = 0
    while 1:
        if subp.poll() == 0:
            logger.debug("{} finished".format(cmd_type))
            subp_status = int(subp.poll())
            break
        elif subp.poll() is None:
            logger.debug(
                "{} duration += {} second".format(cmd_type, wait_interval_sec)  # noqa
            )  # noqa
            time.sleep(wait_interval_sec)
            duration_sec += wait_interval_sec
            if duration_sec > max_timeout_sec:
                logger.error(
                    "{} duration {} second timeout with max_timeout_sec {}".format(  # noqa
                        cmd_type, duration_sec, max_timeout_sec
                    )
                )
                subp.kill()
                break
        else:
            subp_status = subp.poll()
            logger.fatal(
                "exited with abnormal subprocess status: {}".format(  # noqa
                    subp_status
                )  # noqa
            )
            if subp_status == 139:
                break
            else:
                exit(1)
    logger.debug(
        "{} consume {} seconds to finish".format(cmd_type, duration_sec)  # noqa
    )  # noqa

    cmd_res = None
    if subp_status == 0 or subp_status == 139:
        cmd_res = "".join(subp.communicate())
        logger.debug("cmd_res:{}".format(subp.communicate()))
        cmd_res = cmd_res.split("\n")
        cmd_res = filter(lambda r: r != "", cmd_res)
        cmd_res = list(cmd_res)
    return cmd_res


def run_cmds(cmds, interval_second=0, wait_timeout_second=60):
    cmd_res_dict = dict()
    cmds = list(cmds)
    for cidx in range(len(cmds)):
        cmd = cmds[cidx]
        res = run_cmd(cmd, interval_second, wait_timeout_second)
        cmd_res_dict[cmd] = res
    return cmd_res_dict


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
        cmds = ["ls", "ls -l", "adb devices"]
        cmd_handls = run_cmds(cmds)
        for cidx in range(len(cmds)):
            cmd = cmds[cidx]
            h = cmd_handls[cmd]
            logger.info("cmd_idx:{}, cmd:{}".format(cidx, cmd))
            logger.info(h)

    def test_run_cmd(self):
        cmds = ["ls", "pwd", "adb devices"]
        for cidx in range(len(cmds)):
            cmd = cmds[cidx]
            h = run_cmd(cmd)
            logger.info("cmd_idx:{}, cmd:{}".format(cidx, cmd))
            logger.info(h)


if __name__ == "__main__":
    unittest.main()

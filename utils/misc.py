#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import sys
import unittest

sys.path.append("..")
from core.global_config import logger  # noqa


def pattern_match(text, a, b, contain_a_b=False):
    reg_exp = r"%s(.*?)%s" % (a, b)
    if contain_a_b:
        reg_exp = r"(%s.*%s)" % (a, b)
    m = re.search(reg_exp, text)
    if m:
        return m.group(1)
    return ""


class TestMisc(unittest.TestCase):
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

    def test_pattern_match_contain(self):
        res = pattern_match("abcdefgh", "b", "g", False)
        logger.info(res)
        self.assertEqual(res, "cdef")

    def test_pattern_match_not_contain(self):
        res = pattern_match("abcdefgh", "b", "g", True)
        logger.info(res)
        self.assertEqual(res, "bcdefg", "NotEqual")

    def test_pattern_match(self):
        text = "abcdefgh"
        contain_a_b_list = [False, True]
        ptn_a = "b"
        ptn_b = "g"

        for contain_a_b in contain_a_b_list:
            res = pattern_match(text, ptn_a, ptn_b, contain_a_b)
            logger.info(
                "text:{}, ptn_a:{}, ptn_b:{}, contain_a_b:{}".format(
                    text, ptn_a, ptn_b, contain_a_b
                )
            )
            logger.info("{} res:{}".format(pattern_match.__name__, res))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re


def pattern_match(text, a, b, contain_a_b=False):
    reg_exp = r'%s(.*?)%s' % (a, b)
    if contain_a_b:
        reg_exp = r'(%s.*%s)' % (a, b)
    m = re.search(reg_exp, text)
    if m:
        return m.group(1)
    return ""


def test_pattern_match():
    from utils.global_var import logger

    text = "abcdefgh"
    contain_a_b_list = [False, True]
    ptn_a = "b"
    ptn_b = "g"

    for contain_a_b in contain_a_b_list:
        res = pattern_match(text, ptn_a, ptn_b, contain_a_b)
        logger.info("text:{}, ptn_a:{}, ptn_b:{}, contain_a_b:{}".format(text, ptn_a, ptn_b, contain_a_b))
        logger.info("{} res:{}".format(pattern_match.__name__, res))


if __name__ == "__main__":
    test_pattern_match()

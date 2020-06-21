#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging


class LoggerCreator:
    def __init__(self, enable_debug=False):
        self.enable_debug = enable_debug
        self.create_logger()

    def create_logger(self):
        logging.basicConfig(format='[%(levelname)-5s %(asctime)s,%(msecs)d %(filename)s:%(lineno)d %(funcName)s] %('
                                   'message)s',
                            datefmt='%d-%m-%Y:%H:%M:%S')
        logging.getLogger().setLevel(logging.DEBUG if self.enable_debug else logging.INFO)
        logger = logging.getLogger()
        return logger

    def get_enable_debug(self):
        return self.enable_debug


def test_logger_creator(use_global_var=True, enable_debug=False):
    print("use_global_var:{}".format(use_global_var))
    if use_global_var:
        # `enable_debug` defined in utils.global_var
        from utils.global_var import logger
        from utils.global_var import logger_creator
    else:
        logger_creator = LoggerCreator(enable_debug)
        logger = logger_creator.create_logger()

    logger.info("get_enable_debug:{}".format(logger_creator.get_enable_debug()))
    logger.debug("This is a debug log")
    logger.info("This is an info log")
    logger.critical("This is critical")
    logger.error("An error occurred\n")


def test_main():
    use_global_var = [True, False]
    enable_debug = [True, False]

    for g in use_global_var:
        for d in enable_debug:
            test_logger_creator(g, d)


if __name__ == "__main__":
    test_main()

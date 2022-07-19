# -*- coding: utf-8 -*-
import os
import unittest

from relax.log_manager.log import Log


class TestLog(unittest.TestCase):
    _TEST_LOG_FILE_NAME = os.path.join(os.path.curdir, "test_log.log")

    def setUp(self):
        Log(self._TEST_LOG_FILE_NAME, level=1).init()

    def test_write_log(self):
        phase_log_string = "test write log"
        error_log_string = "test error"
        error_log_string2 = "test error 2"
        warn_log_string = "test warn"
        info_log_string = "test info"
        debug_log_string = "test debug"

        # 写不同级别的日志
        Log().phase(phase_log_string)
        Log().error(error_log_string, error_log_string2)
        Log().warn(warn_log_string)
        Log().info(info_log_string)
        Log().debug(debug_log_string)

        with open(self._TEST_LOG_FILE_NAME, "r") as f:
            log_content = f.read()

        phase_log_location = log_content.find("======== %s ========" % phase_log_string)
        error_log_location = log_content.find(error_log_string + " " + error_log_string2)
        warn_log_location = log_content.find(warn_log_string)
        info_log_location = log_content.find(info_log_string)
        debug_log_location = log_content.find(debug_log_string)

        self.assertNotEqual(phase_log_location, -1)
        self.assertNotEqual(error_log_location, -1)
        self.assertNotEqual(warn_log_location, -1)
        self.assertNotEqual(info_log_location, -1)
        self.assertEqual(debug_log_location, -1)

        self.assertNotEqual(Log().get_latest_logs(), "")

    def tearDown(self):
        os.remove(self._TEST_LOG_FILE_NAME)

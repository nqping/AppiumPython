#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Author  : nqp
@File    : NextMessageTest.py
@desc    : 
"""

from Bases.BaseRunner import ParametrizedTestCase

class NextMessageTest(ParametrizedTestCase):

    def testMessages(self):
        # self.driver.find_element_by_android_uiautomator('new UiSelector().text("Messages")').click()
        self.driver.find_element_by_id("com.microsoft.next:id/activity_settingactivity_grid_feedback_container").click()
        self.driver.find_element_by_id("com.microsoft.next:id/include_layout_settings_header_back").click()

    def testCheckupdate(self):
        self.driver.find_element_by_id("com.microsoft.next:id/activity_settingactivity_grid_checkupdate_container").click()

    @classmethod
    def setUpClass(cls):
        super(NextMessageTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(NextMessageTest, cls).tearDownClass()
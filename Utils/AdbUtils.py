#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Author  : nqp
@File    : AdbUtils.py
@desc    : 
"""

import subprocess,os

class AndroidDebugBridge(object):

    def get_devices(self):
        '''获取在线设备'''
        all_devices = []
        cmd = "adb devices"
        reslut = os.popen(cmd).readlines()[1:]
        for item in reslut:
            if item != "\n":
                all_devices.append(str(item).split("\t")[0])
        return all_devices

    def get_status(self):  # 获取设备状态
        cmd1 = 'adb get-state'
        devices_status = os.popen(cmd1).read().split()[0]
        return devices_status




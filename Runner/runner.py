#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@Author  : nqp
@File    : runner.py
@desc    : 
"""
import random
import sys,os
import platform
import unittest
from datetime import datetime
from Bases.BaseAppiumServer import AppiumServer
from Bases.BaseRunner import ParametrizedTestCase
from Utils.AdbUtils import *
from Utils.AndroidUtils import getPhoneInfo
from multiprocessing import Pool
from TestCases.NextMessageTest import NextMessageTest

sys.path.append("..")

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def kill_adb():
    if platform.system() == "Windows":
        # os.popen("taskkill /f /im adb.exe")
        os.system(PATH("../app/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")



def runnerCaseApp(devices):
    starttime = datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(NextMessageTest, param=devices))
    # suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices)) #加入测试类
    unittest.TextTestRunner(verbosity=2).run(suite)
    # endtime = datetime.now()
    # countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "秒")

def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        _initApp["deviceName"] = getDevices[i]["devices"]
        _initApp["platformVersion"] = getPhoneInfo(devices=_initApp["deviceName"])["release"]
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]
        # _initApp["app"] = getDevices[i]["app"]

        # print(f'app=={getDevices[i]["app"]}')
        # apkInfo = ApkInfo(_initApp["app"])
        # _initApp["appPackage"] = apkInfo.getApkBaseInfo()[0]
        # _initApp["appActivity"] = apkInfo.getApkActivity()

        _initApp["appPackage"] = "com.microsoft.next"
        _initApp["appActivity"] = "com.microsoft.next.activity.SettingActivity"
        _initApp["udid"] = getDevices[i]["devices"]
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()

def init(devices):
    # 每次都重新安装uiautomator2都两个应用
    os.popen("adb -s %s uninstall io.appium.uiautomator2.server.test" % devices)
    os.popen("adb -s %s uninstall io.appium.uiautomator2.server" % devices)
    os.popen("adb -s %s install -r %s" % (devices, PATH("../app/appium-uiautomator2-server-v0.1.9.apk")))
    os.popen("adb -s %s install -r %s" % (devices, PATH("../app/appium-uiautomator2-server-debug-androidTest.apk")))
    # os.popen("adb install -r "+PATH("../app/android-system-webview-60.apk"))

if __name__ == '__main__':
    kill_adb()

    devices = AndroidDebugBridge().get_devices()
    if len(devices) > 0:
        l_devices = []
        for dev in devices:
            app = {}
            app["devices"] = dev
            init(dev)
            app["port"] = str(random.randint(4700, 4900))
            app["bport"] = str(random.randint(4700, 4900))
            app["systemPort"] = str(random.randint(4700, 4900))
            # app["app"] = PATH("../app/com.ximalaya.ting.android.apk")  # 测试的app路径,喜马拉雅app

            l_devices.append(app)
        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
    else:
        print("没有可用的安卓设备")



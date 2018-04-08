#coding=utf-8
#!/usr/bin/env monkeyrunner

from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice
from com.android.monkeyrunner.recorder import MonkeyRecorder as recorder
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
import os
import time
import sys
import threading

try:
    print "wait for device connection"
    devicelists = []
    f = open("devices.txt")#读取文件
    for i in f.readlines():
        print i
        if i:
            devicelists.append(mr.waitForConnection(5,i))
            if not devicelists:
                print >> sys.stderr,"fail"
                sys.exit(1)
            else:
                print 'connnect success'
    f.close()
except:
    print "device does not connected"

def ad():
    os.system("adb shell am broadcast -a com.xiaomi.ad.intent.DEBUG_ON")
    print "debug on"
    os.system("adb shell am broadcast -a com.xiaomi.ad.intent.STAGING_ON")
    print "staging on"
    os.system("adb shell am broadcast -a com.xiaomi.ad.intent.FETCH_SPLASH_CONFIG")
    print "splash config"

    #开屏广告
    a = open('activity.txt','r')
    for i in a.readlines():
        print i
        device.startActivity(i)
        mr.sleep(6)
        device.press('KETCODE_BACK',MonkeyDevice.DOWN_AND_UP)
        mr.sleep(3)

    #通知通告
    device.startActivity("com.xiaomi.ad.controller/.MainActivity")
    mr.sleep(2)
    device.touch(480,55,MonkeyDevice.DOWN_AND_UP)
    time.sleep(1)
    device.touch(330,510,MonkeyDevice.DOWN_AND_UP)
    mr.sleep(2)
    device.press('KETCODE_BACK',MonkeyDevice.DOWN_AND_UP)
    time.sleep(1)
    device.press('KETCODE_BACK',MonkeyDevice.DOWN_AND_UP)
    mr.sleep(2)

    #换肤广告
    os.system('adb shell am startservice -n com.miui.systemAdSolution/com.xiaomi.ad.internal.server.WakeupService --es command "cacheUnifiedAd"')
    mr.sleep(2)
    device.startActivity("com.miui.securitycenter/com.miui.securityscan.MainActivity")
    mr.sleep(2)
    kill = os.system("adb shell am force-stop com.miui.securitycenter")
    mr.sleep(5)
    if kill == 0:
        print("has killed")
    else:
        os.system("adb shell am force-stop com.miui.securitycenter")
    device.startActivity("com.miui.securitycenter/com.miui.securityscan.MainActivity")
    mr.sleep(6)
    device.press('KETCODE_BACK',MonkeyDevice.DOWN_AND_UP)
    mr.sleep(2)

while True:
    for i in range(1,11):
        ad()
        print("%d" % i)
        if i > 9:
            os.system("adb shell dumpsys meminfo com.miui.systemAdSolution >> msa.txt")
            os.system("adb shell dumpsys meminfo com.miui.systemAdSolution:ui >> msa_ui.txt")

#-*- coding: utf-8 -*-
import os
import time

def mkdir(path):
    folder = os.path.exists(path)
    if  not folder:
        os.makedirs(path)
        pass
    else:
        print("there is this folder")
    pass

pkglist = []
pkglist = raw_input("Please enter packagename:").split(" ")
print(pkglist)
def mem():
    os.system("adb shell dumpsys meminfo " + i + " >> ./result/meminfo_" + i + ".txt")
    pass

def cpu():
    os.system("adb shell dumpsys cpuinfo " + i + " >> ./result/cpuinfo_" + i + ".txt")

def pid():
    pid = os.popen("adb shell ps | findstr " + i + "").readlines()
    for p in pid:
        if p.split()[8] == i:
            return p.split()[1]
    pass

def uid():
    i_pid = pid()
    #print(i_pid)
    if i_pid:
        uidline = os.popen("adb shell cat /proc/" + i_pid + "/status").readlines()
        #print(uidline)
        for x in uidline:
            if len(x.split()) >= 3 and x.split()[0] == "Uid:":
                #print(x.split()[1])
                return x.split()[1]
    pass
def flow():
    i_uid = uid()
    #print(i_uid + "--------------")
    os.system("adb shell cat /proc/net/xt_qtaguid/stats | findstr "+ i_uid +" >> ./result/flowinfo_" + i + ".txt")
    pass

file = "./result"
mkdir(file)

starttime = time.time()
#print(starttime)

while True:
    currenttime = time.time()
    #print(currenttime)
    t = currenttime - starttime
    #print(t)
    #if int(t) == int(10):
    for i in pkglist:
        if i:
            print(i)
            mem()
            cpu()
            flow()
        else:
            print("not collect time")

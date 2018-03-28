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
pkglist = input("Please enter packagename:").split(" ")
#pkglist = raw_input("Please enter packagename:").split(" ")
#print(pkglist)
def mem(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    os.system("adb shell dumpsys meminfo %s >> ./result/meminfo_%s.txt" % (packagename,filename))
    pass

def cpu(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    os.system("adb shell dumpsys cpuinfo | findstr %s >> ./result/cpuinfo_%s.txt" % (packagename,filename))

def pid(packagename):
    pid = os.popen("adb shell ps | findstr %s" % packagename).readlines()
    for p in pid:
        if p.split()[8] == i:
            return p.split()[1]
    pass

def uid(packagename):
    i_pid = pid(packagename)
    #print(i_pid)
    if i_pid:
        uidline = os.popen("adb shell cat /proc/" + i_pid + "/status").readlines()
        #print(uidline)
        for x in uidline:
            if len(x.split()) >= 3 and x.split()[0] == "Uid:":
                #print(x.split()[1])
                return x.split()[1]
    pass
def flow(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    i_uid = uid(packagename)
    #print(i_uid)
    if i_uid:
        os.system("adb shell cat /proc/net/xt_qtaguid/stats | findstr %s >> ./result/flowinfo_%s.txt" %(i_uid,filename))
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
    if int(t) == int(5):
        for i in pkglist:
            if i:
                #print(i)
                mem(i)
                cpu(i)
                flow(i)
    #else:
        #print("not collect time")

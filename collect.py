#-*- coding: utf-8 -*-
import os
import time
import xlrd
from xlrd import open_workbook
import xdrlib,sys
import xlwt
from xlwt import *
from xlutils.copy import copy

def mkdir(path):
    folder = os.path.exists(path)
    if  not folder:
        os.makedirs(path)
        pass
    else:
        print("there is this folder")
    pass

count = int(input("Please enter run times:"))
interval = int(input("Please enter collect interval:"))

pkglist = []
pkglist = input("Please enter packagename:").split(" ")
#pkglist = raw_input("Please enter packagename:").split(" ")
#print(pkglist)

def mem(packagename):
    mem = os.popen("adb shell dumpsys meminfo %s" % packagename).readlines()
    if mem != []:
        for m in mem:
            if len(m.split()) >= 1 and m.split()[0] == "Native":
                book = xlrd.open_workbook(bookname)
                sheet = book.sheet_by_index(0)
                wb = copy(book)
                ws = wb.get_sheet(0)
                ws.write(0,0,"Native:")
                ws.write(0,1,int(m.split()[2]))
                wb.save(bookname)
            elif len(m.split()) >= 1 and m.split()[0] == "Dalvik":
                book = xlrd.open_workbook(bookname)
                sheet = book.sheet_by_index(0)
                wb = copy(book)
                ws = wb.get_sheet(0)
                ws.write(0,2,"Dalvik")
                ws.write(0,3,int(m.split()[2]))
                wb.save(bookname)
            elif len(m.split()) >= 1 and m.split()[0] == "TOTAL":
                book = xlrd.open_workbook(bookname)
                sheet = book.sheet_by_index(0)
                wb = copy(book)
                ws = wb.get_sheet(0)
                ws.write(0,4,"TOTAL")
                ws.write(0,5,int(m.split()[1]))
                wb.save(bookname)
    else:
        book = xlrd.open_workbook(bookname)
        sheet = book.sheet_by_index(0)
        wb = copy(book)
        ws = wb.get_sheet(0)
        ws.write(0,0,"Native:")
        ws.write(0,1,int(0))
        ws.write(0,2,"Dalvik")
        ws.write(0,3,int(0))
        ws.write(0,4,"TOTAL")
        ws.write(0,5,int(0))
        wb.save(bookname)
    pass

def cpu(packagename):
    print(packagename)
    cpu = os.popen("adb shell dumpsys cpuinfo | findstr %s" % packagename).readlines()
    print(cpu)
    if cpu != []:
        for c in cpu:
            book = xlrd.open_workbook(bookname)
            sheet = book.sheet_by_index(1)
            if len(c.split()) >= 1:
                wb = copy(book)
                ws = wb.get_sheet(1)
                ws.write(0,0,"Total")
                ws.write(0,1,c.split()[0])
                ws.write(0,2,"User")
                ws.write(0,3,c.split()[2])
                ws.write(0,4,"kernel")
                ws.write(0,5,c.split()[5])
                wb.save(bookname)
    else:
        book = xlrd.open_workbook(bookname)
        sheet = book.sheet_by_index(1)
        wb = copy(book)
        ws = wb.get_sheet(1)
        ws.write(0,0,"Total")
        ws.write(0,1,int(0))
        ws.write(0,2,"User")
        ws.write(0,3,int(0))
        ws.write(0,4,"kernel")
        ws.write(0,5,int(0))
        wb.save(bookname)

def pid(packagename):
    pid = os.popen("adb shell ps | findstr %s" % packagename).readlines()
    for p in pid:
        if len(p.split()) >= 1 and p.split()[8] == packagename:
            print("pid" + p.split()[1] )
            return p.split()[1]
    pass

def uid(packagename):
    i_pid = pid(packagename)
    print("uid" + i_pid)
    if i_pid:
        uidline = os.popen("adb shell cat /proc/" + i_pid + "/status").readlines()
        print(uidline)
        for x in uidline:
            if len(x.split()) >= 1 and x.split()[0] == "Uid:":
                #print(x.split()[1])
                return x.split()[1]
    pass

def flow(packagename):
    i_uid = uid(packagename)
    print(i_uid)
    if i_uid:
        flow = os.popen("adb shell cat /proc/net/xt_qtaguid/stats | findstr %s" %i_uid).readlines()
        print(flow)
        if flow != []:
            for f in flow:
                if len(f.split()) >= 1 and f.split()[1] == "wlan0":
                    print("--------" + f.split()[5])
                    print("++++++++" + f.split()[7])
                    total = int(f.split()[5]) + int(f.split()[7])
                    book = xlrd.open_workbook(bookname)
                    sheet = book.sheet_by_index(2)
                    wb = copy(book)
                    ws = wb.get_sheet(2)
                    ws.write(0,0,"rx_bytes")
                    ws.write(0,1,int(f.split()[5]))
                    ws.write(0,2,"tx_bytes")
                    ws.write(0,3,int(f.split()[7]))
                    ws.write(0,4,"Total")
                    ws.write(0,5,total)
                    wb.save(bookname)
                elif len(f.split()) >= 1 and x.split()[1] == "rmnet0":
                    total = int(f.split()[5]) + int(f.split()[7])
                    book = xlrd.open_workbook(bookname)
                    sheet = book.sheet_by_index(2)
                    wb = copy(book)
                    ws = wb.get_sheet(2)
                    ws.write(0,0,"rx_bytes")
                    ws.write(0,1,f.split()[5])
                    ws.write(0,2,"tx_bytes")
                    ws.write(0,3,f.split()[7])
                    ws.write(0,4,"Total")
                    ws.write(0,5,total)
                    wb.save(bookname)
        else:
            book = xlrd.open_workbook(bookname)
            sheet = book.sheet_by_index(2)
            wb = copy(book)
            ws = wb.get_sheet(2)
            ws.write(0,0,"rx_bytes")
            ws.write(0,1,int(0))
            ws.write(0,2,"tx_bytes")
            ws.write(0,3,int(0))
            ws.write(0,4,"Total")
            ws.write(0,5,int(0))
            wb.save(bookname)
            print("11111111111111111111")
    pass

file = "./result"
mkdir(file)

for n in pkglist:
    if n:
        filename = n
        invaild_char = '\\/:*?<>"|'
        for i in invaild_char:
            filename = filename.replace(i,"_")
        bookname = "./result/"+filename+"_info.xls"
        book = xlwt.Workbook(bookname)
        sheet = book.add_sheet('meminfo',cell_overwrite_ok=True)
        sheet_2 = book.add_sheet('cpuinfo',cell_overwrite_ok=True)
        sheet_3 = book.add_sheet('flowinfo',cell_overwrite_ok=True)
        book.save(bookname)

c_count = 0
while True:
    for i in pkglist:
        if i:
            print(i)
            mem(i)
            cpu(i)
            flow(i)
    c_count += 1
    print(c_count)
    time.sleep(interval)
    if c_count == count:
        print("test end")
        break

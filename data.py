#-*- coding: utf-8 -*-
import os
import time
import xlwt
import codecs
import math

book = xlwt.Workbook()

def data_mem(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    sheet= book.add_sheet('meminfo',cell_overwrite_ok=True)
    title = ['Native','Dalvik','Total']
    lie = 0
    for l in title:
        sheet.write(0,lie,l)
        lie += 1
    row = 1
    col = 0
    f = codecs.open('./result/meminfo_%s.txt' % filename,'r')
    f = f.readlines()[25:]
    for i in f:
        i = i.split()
        if len(i) > 1:
            if i[0] == "Java" and i[1] == "Heap:":
                print("N"+i[2])
                sheet.write(row,col,int(i[2]))
            elif i[0] == "Native" and i[1] == "Heap:":
                print("b"+i[2])
                sheet.write(row,col+1,int(i[2]))
            elif i[0] == "TOTAL:":
                print("t"+i[1])
                sheet.write(row,col+2,int(i[1]))
                row += 1
                continue
        else:
            continue
    book.save('%s.xls' % filename)

def data_cpu(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    sheet = book.add_sheet('cpuinfo',cell_overwrite_ok=True)
    title = ['Total','User','kernel']
    lie = 0
    for l in title:
        sheet.write(0,lie,l)
        lie += 1
    row = 1
    col = 0
    f = codecs.open('./result/cpuinfo_%s.txt' % filename,'r')
    for i in f:
        i = i.split()
        if i:
            sheet.write(row,col,i[0])
            sheet.write(row,col+1,i[2])
            sheet.write(row,col+2,5)
        row += 1
    book.save('%s.xls' % filename)

def data_flow(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    sheet = book.add_sheet('flowinfo',cell_overwrite_ok=True)
    title = ['wlan','rmnet']
    lie = 0
    for l in title:
        sheet.write(0,lie,l)
        lie += 3
    sub_title = ['rx_bytes','tx_bytes','Total']
    sub_lie = 0
    for s in sub_title:
        sheet.write(1,sub_lie,s)
        sheet.write(1,sub_lie+3,s)
        sub_lie += 1
    row = 2
    col = 0
    f = codecs.open('./result/flowinfo_%s.txt' % filename,'r')
    for i in f:
        i = i.split()
        total = int(i[5]) + int(i[7])
        if i[1] == "wlan0":
            sheet.write(row,col,int(i[5]))
            sheet.write(row,col+1,int(i[7]))
            sheet.write(row,col+2,total)
        elif i[1] == "rmnet0":
            col += 3
            sheet.write(row,col,int(i[5]))
            sheet.write(row,col+1,int(i[7]))
            sheet.write(row,col+2,total)
        row += 1
    book.save('%s.xls' % filename)

#-*- coding: utf-8 -*-
import os
import time
import xlwt
import codecs
import math
import pandas
import numpy

book = xlwt.Workbook()

def data_mem(packagename):
    #print("-----------"+packagename)
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    #print("-----------"+filename)
    sheet= book.add_sheet('%s_m'% filename,cell_overwrite_ok=True)
    title = ['Number','Java','Native','Total']
    lie = 0
    for l in title:
        sheet.write(0,lie,l)
        lie += 1
    row = 1
    col = 0
    num = 1
    #print("+++++++++++"+filename)
    f = codecs.open('./result/meminfo_%s.txt'% filename,'r')
    f = f.readlines()[25:]
    for i in f:
        i = i.split()
        if len(i) > 1:
            if i[0] == "Java" and i[1] == "Heap:":
                #print("N"+i[2])
                sheet.write(row,col,int(num))
                num += 1
                sheet.write(row,col+1,int(i[2]))
            elif i[0] == "Native" and i[1] == "Heap:":
                #print("b"+i[2])
                sheet.write(row,col+2,int(i[2]))
            elif i[0] == "TOTAL:":
                #print("t"+i[1])
                sheet.write(row,col+3,int(i[1]))
                row += 1
                continue
        else:
            continue
    book.save('./result/performence_info.xls')

def data_cpu(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    sheet = book.add_sheet('%s_c'% filename,cell_overwrite_ok=True)
    title = ['Number','Total','User','kernel']
    lie = 0
    for l in title:
        sheet.write(0,lie,l)
        lie += 1
    row = 1
    col = 0
    num = 1
    f = codecs.open('./result/cpuinfo_%s.txt' % filename,'r')
    for i in f:
        i = i.split()
        if i and i[1].split("/")[1][:-1] == packagename:
            sheet.write(row,col,int(num))
            num += 1
            sheet.write(row,col+1,i[0].split("%")[0])
            sheet.write(row,col+2,i[2].split("%")[0])
            sheet.write(row,col+3,i[5].split("%")[0])
            row += 1
    book.save('./result/performence_info.xls')

def data_flow(packagename):
    filename = packagename
    invaild_char = '\\/:*?<>"|'
    for i in invaild_char:
        filename = filename.replace(i,"_")
    sheet = book.add_sheet('%s_f'% filename,cell_overwrite_ok=True)
    title = ['wlan','rmnet']
    lie = 1
    for l in title:
        sheet.write(0,lie,l)
        lie += 3
    sheet.write(1,0,"Number")
    sub_title = ['rx_bytes','tx_bytes','Total']
    sub_lie = 1
    for s in sub_title:
        sheet.write(1,sub_lie,s)
        sheet.write(1,sub_lie+3,s)
        sub_lie += 1
    row = 2
    col = 0
    num = 1
    f = codecs.open('./result/flowinfo_%s.txt' % filename,'r')
    for i in f:
        i = i.split()
        if i:
            total = int(i[5]) + int(i[7])
            sheet.write(row,col,int(num))
            num += 1
            if i[1] == "wlan0":
                sheet.write(row,col+1,int(i[5]))
                sheet.write(row,col+2,int(i[7]))
                sheet.write(row,col+3,total)
            elif i[1] == "rmnet0":
                sheet.write(row,col+1,int(i[5]))
                sheet.write(row,col+2,int(i[7]))
                sheet.write(row,col+3,total)
            row += 1
    book.save('./result/performence_info.xls')


#data_mem("com.miui.systemAdSolution")
#data_cpu("com.miui.systemAdSolution")
#data_flow("com.miui.systemAdSolution")

#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 處理 rss 裡的 日期時間 資料

import string
import time
import datetime


def datehandle(adate) :
    """ 將 Mon, 18 Mar 2013 14:02:00 +0800 格式的 日期時間 資料 轉成 secs """
    months = {}
    months["JAN"] = 1
    months["FEB"] = 2
    months["MAR"] = 3
    months["APR"] = 4
    months["MAY"] = 5
    months["JUN"] = 6
    months["JUL"] = 7
    months["AUG"] = 8
    months["SEP"] = 9
    months["OCT"] = 10
    months["NOV"] = 11
    months["DEC"] = 12

    date1 = string.split(adate, ",")[1]
    (day, month, year, time1, zone) = string.split(date1)
    
    (hour, minute, sec) = string.split(time1, ":")

    day = string.atoi(day)
    month = months[string.upper(month)]
    year = string.atoi(year)
    hour = string.atoi(hour)
    minute = string.atoi(minute)
    sec = string.atoi(sec)

    aa = datetime.datetime(year, month, day, hour, minute, sec)

    if (zone[0] == "+") :
        delta = datetime.timedelta(hours=string.atoi(zone[1:3]))
        aa -= delta
    elif (zone[0] == "-") :
        delta = datetime.timedelta(hours=string.atoi(zone[1:3]))
        aa += delta

    # 根據系統時區設定 time.timezone 來增減時間
    aa += datetime.timedelta(seconds=time.timezone * (-1))

    # 遇到日期 Mon, 01 Jan 1900 00:00:00 +0800 會出錯, 因此將無法解析的日期定為 1910.01.01
    try :
        secs = time.mktime(aa.timetuple())
    except :
        secs = time.mktime(datetime.date(1910,1,1).timetuple())

    return secs


def datehandle2(adate) :
    """ 將 2013-03-11T19:03:35+08:00 格式的 日期時間 資料 轉成 secs """

    # 如果日期格式為 2013-03-11T19:03:35Z, Z代表 +00:00
    if (string.upper(adate[-1]) == "Z") :
        adate = adate[:-1]+"+00:00"

    (date1, time1) = string.split(adate,"T")
    (year, month, day) = string.split(date1, "-")

    if ("+" in time1) :
        zonekey = "+"
    elif ("-" in time1) :
        zonekey = "-"

    (time2, zone) = string.split(time1, zonekey)
    (hour, minute, sec) = string.split(time2, ":")

    day = string.atoi(day)
    month = string.atoi(month)
    year = string.atoi(year)
    hour = string.atoi(hour)
    minute = string.atoi(minute)

    if (len(sec) > 2 and sec[2] == ".") :
        msec = string.atoi(sec[3:])
        sec = string.atoi(sec[:2])
    else :
        msec = 0
        sec = string.atoi(sec)

    aa = datetime.datetime(year, month, day, hour, minute, sec, msec)

    aa += datetime.timedelta(hours=8)

    if (zonekey == "+") :
        delta = datetime.timedelta(hours=string.atoi(zone[0:2]))
        aa -= delta
    elif (zonekey == "-") :
        delta = datetime.timedelta(hours=string.atoi(zone[0:2]))
        aa += delta

    # 根據系統時區設定 time.timezone 來增減時間
    aa += datetime.timedelta(seconds=time.timezone * (-1))

    # 遇到日期 Mon, 01 Jan 1900 00:00:00 +0800 會出錯, 因此將無法解析的日期定為 1910.01.01
    try :
        secs = time.mktime(aa.timetuple())
    except :
        secs = time.mktime(datetime.date(1910,1,1).timetuple())

    return secs

if __name__ == "__main__" :
    adate1 = "Thu, 21 Feb 2013 07:32:25 +0000"
    adate2 = "Mon, 18 Mar 2013 14:02:00 +0800"
    adate3 = "Mon, 01 Jan 1900 00:00:00 +0800"
    bdate1 = "2013-03-11T19:03:35+08:00"
    bdate2 = "2013-03-11T18:56:00.345+08:00"

    aa = datehandle(adate2)
    # print time.localtime(aa)
    print time.gmtime(aa)

    bb = datehandle2(bdate1)
    # print time.localtime(bb)
    print time.gmtime(bb)

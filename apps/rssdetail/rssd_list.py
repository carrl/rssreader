#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 傳回 rss_detail 的列表

import cgi
import urllib
import string
import sqlite3
import json
import sys

sys.path.append("../common")
import common


# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params

def rssd_dict(atype, hashid="", keyword="", showmode=1, lastid="", tagid=-1, cnt=30) :
    result = {"title":None, "link":None, "hashid":"", "unreadcnt":0, "detail":[]}

    if (atype == 0) :           # 一般情形
        dbname = common.getdbname()

        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = "select id,title,link,hashid,unreadcnt from rss_main where hashid=:hashid"
        cursor.execute(sql, {"hashid": hashid})

        adata = cursor.fetchone()
        if adata :
            mainid = adata[0]
            # print mainid
            result["title"] = adata[1]
            result["link"] = adata[2]
            result["hashid"] = adata[3]
            result["unreadcnt"] = adata[4]

            # 取得 lastid 的 pubdate
            lastpubdate = ""
            if (lastid) :
                cursor1 = dbconn.cursor()
                sql1 = "select pubdate from rss_detail where id=:id"
                cursor1.execute(sql1, {"id": lastid})
                lastpubdate = cursor1.fetchone()[0]
                cursor1.close()

            rssd_list = []
            cursor2 = dbconn.cursor()
            sql2 = "select id,rssid,title,pubdate,readed,star from rss_detail where mainid=:mainid and title<>''"
            if (lastpubdate) :
                sql2 += " and pubdate<:lastpubdate"
            if (showmode == 2) :
                sql2 += " and readed<>1"
            sql2 += " order by pubdate desc"
            sql2 += " limit 0,:cnt"
            cursor2.execute(sql2, {"mainid":mainid, "lastpubdate":lastpubdate, "cnt":cnt})
            bdata = cursor2.fetchone()
            while bdata :
                rsshash = {}
                rsshash["id"] = bdata[0]
                rsshash["rssid"] = bdata[1]
                rsshash["title"] = bdata[2]
                rsshash["pubdate"] = bdata[3]
                rsshash["readed"] = bdata[4]
                rsshash["star"] = bdata[5]
                rssd_list.append(rsshash)
                bdata = cursor2.fetchone()

            cursor2.close()

            result["detail"] = rssd_list

        cursor.close()
        dbconn.close()
    elif (atype == 1) :         # 檢視 星號List
        result["title"] = "星號列表"
        result["hashid"] = ""
        result["unreadcnt"] = 0

        dbname = common.getdbname()

        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        # 建立 rss_main.id 對 title 的 dict
        main_titles = {}
        sql = "select id,title from rss_main"
        cursor.execute(sql)
        adata = cursor.fetchone()
        while adata :
            main_titles[adata[0]] = adata[1]
            adata = cursor.fetchone()

        # 取得 lastid 的 pubdate
        lastpubdate = ""
        if (lastid) :
            cursor1 = dbconn.cursor()
            sql1 = "select pubdate from rss_detail where id=:id"
            cursor1.execute(sql1, {"id": lastid})
            lastpubdate = cursor1.fetchone()[0]
            cursor1.close()

        rssd_list = []
        cursor2 = dbconn.cursor()
        sql2 = "select id,mainid,rssid,title,pubdate,readed,star from rss_detail where star=1 and title<>''"
        if (lastpubdate) :
            sql2 += " and pubdate<:lastpubdate"
        sql2 += " order by pubdate desc"
        sql2 += " limit 0,:cnt"
        cursor2.execute(sql2, {"lastpubdate":lastpubdate, "cnt":cnt})
        bdata = cursor2.fetchone()
        while bdata :
            rsshash = {}
            rsshash["id"] = bdata[0]
            rsshash["main_title"] = main_titles[bdata[1]]
            rsshash["rssid"] = bdata[2]
            rsshash["title"] = bdata[3]
            rsshash["pubdate"] = bdata[4]
            rsshash["readed"] = bdata[5]
            rsshash["star"] = bdata[6]
            rssd_list.append(rsshash)
            bdata = cursor2.fetchone()

        cursor2.close()

        result["detail"] = rssd_list

        cursor.close()
        dbconn.close()
    elif (atype == 2) :         # 搜尋
        result["title"] = "搜尋"
        result["hashid"] = ""
        result["unreadcnt"] = 0

        keyword = urllib.unquote(keyword.decode("utf-8"))

        dbname = common.getdbname()

        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        # 建立 rss_main.id 對 title 的 dict
        main_titles = {}
        sql = "select id,title from rss_main"
        cursor.execute(sql)
        adata = cursor.fetchone()
        while adata :
            main_titles[adata[0]] = adata[1]
            adata = cursor.fetchone()

        # 取得 lastid 的 pubdate
        lastpubdate = ""
        if (lastid) :
            cursor1 = dbconn.cursor()
            sql1 = "select pubdate from rss_detail where id=:id"
            cursor1.execute(sql1, {"id": lastid})
            lastpubdate = cursor1.fetchone()[0]
            cursor1.close()

        rssd_list = []
        cursor2 = dbconn.cursor()
        sql2 = "select id,mainid,rssid,title,pubdate,readed,star from rss_detail where 1=1 and title<>''"
        sql2 += " and (title like :keyword or content like :keyword or author like :keyword)"
        if (lastpubdate) :
            sql2 += " and pubdate<:lastpubdate"
        sql2 += " order by pubdate desc"
        sql2 += " limit 0,:cnt"
        # print sql2
        cursor2.execute(sql2, {"lastpubdate":lastpubdate, "keyword":'%'+keyword+'%', "cnt":cnt})
        bdata = cursor2.fetchone()
        while bdata :
            rsshash = {}
            rsshash["id"] = bdata[0]
            rsshash["main_title"] = main_titles[bdata[1]]
            rsshash["rssid"] = bdata[2]
            rsshash["title"] = bdata[3]
            rsshash["pubdate"] = bdata[4]
            rsshash["readed"] = bdata[5]
            rsshash["star"] = bdata[6]
            rssd_list.append(rsshash)
            bdata = cursor2.fetchone()

        cursor2.close()

        result["detail"] = rssd_list

        cursor.close()
        dbconn.close()
    elif (atype == 3) :         # TAG
        result["title"] = "TAG"
        result["hashid"] = ""
        result["unreadcnt"] = 0

        dbname = common.getdbname()

        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        # TAG 名稱
        sql = "select tname from tags where id=:tagid"
        cursor.execute(sql, {"tagid": tagid})
        adata = cursor.fetchone()
        if adata :
            result["title"] = adata[0]

        # 建立 rss_main.id 對 title 的 dict
        main_titles = {}
        sql = "select id,title from rss_main"
        cursor.execute(sql)
        adata = cursor.fetchone()
        while adata :
            main_titles[adata[0]] = adata[1]
            adata = cursor.fetchone()

        # 取得 lastid 的 pubdate
        lastpubdate = ""
        if (lastid) :
            cursor1 = dbconn.cursor()
            sql1 = "select pubdate from rss_detail where id=:id"
            cursor1.execute(sql1, {"id": lastid})
            lastpubdate = cursor1.fetchone()[0]
            cursor1.close()

        rssd_list = []
        cursor2 = dbconn.cursor()
        sql2 = "select id,mainid,rssid,title,pubdate,readed,star from rss_detail where mainid in (select rid from tag_detail where tid=:tid) and title<>''"
        if (lastpubdate) :
            sql2 += " and pubdate<:lastpubdate"
        if (showmode == 2) :
            sql2 += " and readed<>1"
        sql2 += " order by pubdate desc"
        sql2 += " limit 0,:cnt"
        cursor2.execute(sql2, {"tid":tagid, "lastpubdate":lastpubdate, "cnt":cnt})
        bdata = cursor2.fetchone()
        while bdata :
            rsshash = {}
            rsshash["id"] = bdata[0]
            rsshash["main_title"] = main_titles[bdata[1]]
            rsshash["rssid"] = bdata[2]
            rsshash["title"] = bdata[3]
            rsshash["pubdate"] = bdata[4]
            rsshash["readed"] = bdata[5]
            rsshash["star"] = bdata[6]
            rssd_list.append(rsshash)
            bdata = cursor2.fetchone()

        cursor2.close()

        result["detail"] = rssd_list

        cursor.close()
        dbconn.close()


    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        atype = string.atoi(params["type"])
    except :
        atype = 0
    # atype = 3

    if (atype == 0) :
        try :
            hashid = params["id"]
        except :
            hashid = ""

    if ((atype == 0) or (atype == 3)) :
        try :
            showmode = string.atoi(params["showmode"])
        except :
            showmode = 1

    try :
        lastid = params["lastid"]

    except :
        lastid = ""

    try :
        keyword = params["keyword"]
    except :
        keyword = ""
    # keyword = "linux"

    try :
        tagid = params["tagid"]
    except :
        tagid = -1
    # tagid = 5

    cnt = 30

    if (atype == 0 and hashid) :           # 一般情形
        rssdl = rssd_dict(0, hashid, "", showmode, lastid, -1, cnt)
    elif (atype == 1) :         # 檢視 星號List
        rssdl = rssd_dict(1, "", "", 0, lastid, -1, cnt)
    elif ((atype == 2) and (keyword != "")) :         # 搜尋
        rssdl = rssd_dict(2, "", keyword, 0, lastid, -1, cnt)
    elif ((atype == 3) and (tagid != -1)) : # TAG
        rssdl = rssd_dict(3, "", "", showmode, lastid, tagid, cnt)
    else :
        rssdl = {}

    # rssdl["params"] = params

    print "Content-type: application/json"
    print

    print json.dumps(rssdl)

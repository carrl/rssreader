#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 傳回 rss_detail 的列表

import cgi
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

def rssd_dict(hashid, showmode=1, lastid="", cnt=30) :
    result = {}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id,title,hashid,unreadcnt from rss_main where hashid=:hashid"
    cursor.execute(sql, {"hashid": hashid})

    adata = cursor.fetchone()
    if adata :
        mainid = adata[0]
        # print mainid
        result["title"] = adata[1]
        result["hashid"] = adata[2]
        result["unreadcnt"] = adata[3]

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
        sql2 = "select id,rssid,title,pubdate,readed from rss_detail where mainid=:mainid and title<>''"
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
        hashid = params["id"]
        showmode = string.atoi(params["showmode"])
    except :
        hashid = ""
        showmode = 1

    try :
        lastid = params["lastid"]
    except :
        lastid = ""

    cnt = 30

    print "Content-type: application/json"
    print

    if (hashid) :
        rssdl = rssd_dict(hashid, showmode, lastid, cnt)
    else :
        rssdl = {}

    print json.dumps(rssdl)

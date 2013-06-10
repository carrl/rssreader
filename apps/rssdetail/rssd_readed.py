#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 記錄已經讀取的資料

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

def rssdetail_readed(aid) :
    result = {"result":"nook" ,"hashid":None, "unreadcnt":0}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "update rss_detail set readed=1 where id=:aid"
    cursor.execute(sql, {"aid": aid})

    dbconn.commit()

    # 找出 mainid
    sql = "select mainid from rss_detail where id=:aid"
    cursor.execute(sql, {"aid": aid})
    adata = cursor.fetchone()
    if adata:
        mainid = adata[0]
    else :
        mainid = -1

    # 根據 mainid, 將 rss_main.unreadcnt - 1
    if (mainid != -1) :
        sql = "select count(*) from rss_detail where mainid=:mainid and readed<>1"
        cursor.execute(sql, {"mainid":mainid})
        adata = cursor.fetchone()
        unread = adata[0]

        sql = "update rss_main set unreadcnt=:unread where id=:id"
        cursor.execute(sql, {"id":mainid, "unread":unread})
        dbconn.commit()

        sql = "select id,hashid,unreadcnt from rss_main where id=:id"
        cursor.execute(sql, {"id":mainid})
        adata = cursor.fetchone()
        if adata :
            result["result"] = "ok"
            result["hashid"] = adata[1]
            result["unreadcnt"] = adata[2]
        
    cursor.close()
    dbconn.close()

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    print "Content-type: application/json"
    print

    try :
        aid = params["id"]
        rr = rssdetail_readed(aid)
        print json.dumps(rr)
    except :
        aid = ""
        print json.dumps("{'result': 'nook'}")


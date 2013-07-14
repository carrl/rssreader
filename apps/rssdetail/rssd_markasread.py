#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 將 所有 item 都改為 已閱讀

import cgi
import json
import string
import sqlite3
import sys

sys.path.append("../common")
import common


# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params

def markasread(hashid, lastdate) :
    result = {"result": "nook"}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id,hashid from rss_main where hashid=:hashid"
    cursor.execute(sql, {"hashid":hashid})

    adata = cursor.fetchone()
    if adata :
        aid = adata[0]

        # 將某 hashid 的所有 子item 改為已閱讀
        cursor2 = dbconn.cursor()
        sql2 = "update rss_detail set readed=1 where mainid=:mainid and pubdate<=:lastdate and readed<>1"
        cursor2.execute(sql2, {"mainid":aid, "lastdate":lastdate})
        dbconn.commit()

        # 重新計算 未讀 count
        cursor2.execute("select count(*) from rss_detail where mainid=:mainid and readed<>1", {"mainid":aid})
        bdata = cursor2.fetchone()
        if bdata :
            unreadcnt = bdata[0]
        else :
            unreadcnt = 0

        # 更新 未讀 count
        sql3 = "update rss_main set unreadcnt=:unreadcnt where hashid=:hashid"
        cursor2.execute(sql3, {"hashid":hashid, "unreadcnt":unreadcnt})
        dbconn.commit()

        cursor2.close()

        result["result"] = "ok"
        result["id"] = aid

    cursor.close()
    dbconn.close()

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        hashid = params["id"]
    except :
        hashid = ""

    try :
        lastdate = string.atoi(params["lastdate"])
    except :
        lastdate = -1

    if (hashid and lastdate != -1) :
        result = markasread(hashid, lastdate)
    else :
        result = {"result": "nook"}

    print "Content-type: application/json"
    print

    print json.dumps(result)

#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 將 所有 item 都改為 已閱讀

import cgi
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

def markasread(hashid) :
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
        sql2 = "update rss_detail set readed=1 where mainid=:mainid"
        cursor2.execute(sql2, {"mainid":aid})

        # 更新 未讀 count
        sql3 = "update rss_main set unreadcnt=0 where hashid=:hashid"
        cursor2.execute(sql3, {"hashid":hashid})

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

    if hashid :
        result = markasread(hashid)
    else :
        result = {"result": "nook"}

    print "Content-type: application/json"
    print

    print result

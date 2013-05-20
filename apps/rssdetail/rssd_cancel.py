#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 取消訂閱

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

def rssd_cancel(hashid) :
    # 刪除 rss_main 及 rss_detail 中關於 hashid 的資料
    result = {"result": "ok"}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql0 = "select id from rss_main where hashid=:hashid"
    cursor.execute(sql0, {"hashid": hashid})
    adata = cursor.fetchone()
    if adata :
        mainid = adata[0]
    else :
        mainid = 0

    if (mainid != 0) :
        sql1 = "delete from rss_main where id=:mainid"
        cursor.execute(sql1, {"mainid": mainid})

        sql2 = "delete from rss_detail where mainid=:mainid"
        cursor.execute(sql2, {"mainid": mainid})

        dbconn.commit()

    cursor.close()
    dbconn.close()

    return result
    

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        hashid = params["id"]
    except :
        hashid = ""

    if (hashid) :
        result = rssd_cancel(hashid)
    else :
        result = {"result": "nook"}

    print "Content-type: application/json"
    print

    print json.dumps(result)


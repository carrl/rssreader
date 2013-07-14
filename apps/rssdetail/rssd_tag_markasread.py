#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 將 某TAG的 所有 item 都改為 已閱讀

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

def tag_markasread(tagid, lastdate) :
    result = {"result": "nook"}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    try :
        # 將某 tag 的所有 子item 改為已閱讀

        sql = "update rss_detail set readed=1 where mainid in (select rid from tag_detail where tid=:tagid) and pubdate<=:lastdate and readed<>1"
        cursor.execute(sql, {"tagid":tagid, "lastdate":lastdate})
        dbconn.commit()

        sql = "select rid from tag_detail where tid=:tagid"
        cursor.execute(sql, {"tagid":tagid})
        adata = cursor.fetchone()
        while adata :
            aid = adata[0]

            cursor2 = dbconn.cursor()
            # 重新計算 未讀 count
            cursor2.execute("select count(*) from rss_detail where mainid=:mainid and readed<>1", {"mainid":aid})
            bdata = cursor2.fetchone()
            if bdata :
                unreadcnt = bdata[0]
            else :
                unreadcnt = 0

            # 更新 未讀 count
            sql2 = "update rss_main set unreadcnt=:unreadcnt where id=:aid"
            cursor2.execute(sql2, {"aid":aid, "unreadcnt":unreadcnt})
            dbconn.commit()

            cursor2.close()

            adata = cursor.fetchone()

        result["result"] = "ok"
    except :
        pass

    cursor.close()
    dbconn.close()

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        tagid = params["tagid"]
    except :
        tagid = ""

    try :
        lastdate = string.atoi(params["lastdate"])
    except :
        lastdate = -1

    if (tagid and lastdate != -1) :
        result = tag_markasread(tagid, lastdate)
    else :
        result = {"result": "nook"}

    print "Content-type: application/json"
    print

    print json.dumps(result)

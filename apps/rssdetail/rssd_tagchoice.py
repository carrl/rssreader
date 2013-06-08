#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 將收集的 rss網站 加上 TAG

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

def rssd_tagchoice(hashid,tagid,sel) :
    """
    將收集的 rss網站 加上 TAG
    當 tagid 或 sel 其中一個為 -1 時, 只查詢目前 TAG 情形
    """
    result = {"result":"nook", "tagselected":None}

    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id from rss_main where hashid=:hashid"
    cursor.execute(sql, {"hashid":hashid})
    adata = cursor.fetchone()
    if adata :
        mainid = adata[0]
    else :
        mainid = ""

    if (mainid) :
        if ((tagid != -1) and (sel != -1)) :
            sql = "select count(rid) from tag_detail where rid=:rid and tid=:tid"
            cursor.execute(sql, {"rid":mainid, "tid":tagid})
            adata = cursor.fetchone()
            acnt = adata[0]

            if (sel == 1) :         # 增加 TAG
                if (acnt == 0) :
                    sql = "insert into tag_detail(rid,tid) values(:rid, :tid)"
                    cursor.execute(sql, {"rid":mainid, "tid":tagid})
                    dbconn.commit()
            else :                  # 刪除 TAG
                if (acnt > 0) :
                    sql = "delete from tag_detail where rid=:rid and tid=:tid"
                    cursor.execute(sql, {"rid":mainid, "tid":tagid})
                    dbconn.commit()

        tagselected = []
        sql = "select tid from tag_detail where rid=:rid"
        cursor.execute(sql, {"rid":mainid})
        adata = cursor.fetchone()
        while adata :
            tagselected.append(adata[0])
            adata = cursor.fetchone()

        result["result"] = "ok"
        result["tagselected"] = tagselected

    cursor.close()
    dbconn.close()

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        hashid = params["hashid"]
    except :
        hashid = ""

    try :
        tagid = string.atoi(params["tagid"])
        sel = string.atoi(params["sel"])
    except :
        tagid = -1
        sel = -1

    if (hashid) :
        result = rssd_tagchoice(hashid, tagid, sel)
    else :
        result = {"result":"nook", "tagselected":None}

    # result["params"] = params

    print "Content-type: application/json"
    print

    print json.dumps(result)


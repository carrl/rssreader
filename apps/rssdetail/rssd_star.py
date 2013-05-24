#! /usr/bin/env python
#-*- coding:utf-8 -*-
# rss_detail 加上星號 或 不加星號

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


def rssd_star(aid, star=0) :
    """ 將 rss_detail 的 id 這筆記錄 加上星號 或 不加星號 """
    result = {}

    try :
        dbname = common.getdbname()

        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = "update rss_detail set star=:star where id=:id"
        cursor.execute(sql, {"star":star, "id":aid})
        dbconn.commit()

        cursor.close()
        dbconn.close()

        result["result"] = "ok"
    except e :
        result["result"] = e
        

    return result


if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        aid = params["id"]
        star = params["star"]
    except :
        aid = ""
        star = 0

    if (aid) :
        result = rssd_star(aid, star)
    else :
        result = {"result":"nook"}

    print "Content-type: application/json"
    print

    print json.dumps(result)


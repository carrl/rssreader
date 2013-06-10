#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 更改 TAG 名稱

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

def tag_rename(tagid, newname) :
    result = {"result": "nook"}
    dbname = common.getdbname()

    try :
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = "update tags set tname=:newname where id=:tagid"
        cursor.execute(sql, {"tagid":tagid, "newname":newname})

        dbconn.commit()
        cursor.close()
        dbconn.close()

        result["result"] = "ok"
    except :
        pass

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        tagid = params["tagid"]
    except :
        tagid = ""

    try :
        newname = params["newname"]
    except :
        newname = ""

    if (tagid and newname) :
        result = tag_rename(tagid, newname)
    else :
        result = {"result": "nook"}

    print "Content-type: application/json"
    print

    print json.dumps(result)

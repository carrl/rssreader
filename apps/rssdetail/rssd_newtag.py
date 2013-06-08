#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 新增 TAG

import cgi
import string
import sqlite3
import json
import sys
import urllib

sys.path.append("../common")
import common

# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params


def rssd_newtag(tagname) :
    """ 新增 TAG """
    result = {"result": "nook", "taglist": None}

    tagname = urllib.unquote(tagname.decode("utf-8"))

    dbname = common.getdbname()

    try :
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = "select count(*) from tags where tname=:tname"
        cursor.execute(sql, {"tname": tagname})
        adata = cursor.fetchone()
        if (adata[0] == 0) :
            sql = "insert into tags(tname) values(:tagname)"
            cursor.execute(sql, {"tagname": tagname})
            dbconn.commit()

        taglists = []
        sql = "select id,tname from tags order by tname"
        cursor.execute(sql)
        adata = cursor.fetchone()
        while adata :
            taglists.append({"id":adata[0], "name":adata[1]})
            adata = cursor.fetchone()

        cursor.close()
        dbconn.close()

        result["result"] = "ok"
        result["taglist"] = taglists
    except :
        pass

    return result


if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        tagname = params["tagname"]
    except :
        tagname = ""

    if tagname :
        result = rssd_newtag(tagname)
    else :
        result = {"result": "nook", "taglist": None}

    print "Content-type: application/json"
    print

    print json.dumps(result)

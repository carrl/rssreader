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


def rssd_taglist() :
    """ TAG List """
    result = {"result": "nook", "taglist": None}

    dbname = common.getdbname()

    try :
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

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
    result = rssd_taglist()

    print "Content-type: application/json"
    print

    print json.dumps(result)

#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 網站用 rss2db 程式

import cgi
import os
import string
import sys

import rss2db

sys.path.append("../common")
import common


# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params


if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        hashid = params["id"]
    except :
        hashid = ""

    if (hashid) :
        dbname = common.getdbname()
        if (dbname and os.path.exists(dbname)) :
            rss2db = rss2db.Rss2DB(dbname, showmsg=False)

            rss2db.updatesingle(hashid)

    print "Content-type: application/json"
    print

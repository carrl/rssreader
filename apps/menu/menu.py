#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 產生 menu 資料 (json)

import json
import sqlite3
import sys

sys.path.append("../common")
import common


def rsslist() :
    rsslist_array = []
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id,title,hashid,unreadcnt from rss_main order by id"
    cursor.execute(sql)
    adata = cursor.fetchone()
    while adata :
        aid = adata[0]
        atitle = adata[1]
        alink = adata[2]
        unread = adata[3]

        rsslist_array.append({"title":atitle, "link":alink, "unread":unread})
        adata = cursor.fetchone()

    cursor.close()
    dbconn.close()

    return rsslist_array

if __name__ == "__main__" :
    print "Content-type: application/json"
    print

    rsslist = rsslist()

    search = common.getsearch()
    # menuobj = [{"title": "訂閱", "sub": rsslist}]
    menuobj = [{"title":"星號", "link":"star", "sub":[]}, {"title":"訂閱", "sub":rsslist}]
    if (search) :
        menuobj.insert(0, {"title":"搜尋", "link":"search", "sub":[]})

    print json.dumps(menuobj)

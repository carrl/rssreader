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

def rsstags() :
    rsstags_array = []

    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id,tname from tags order by tname"
    cursor.execute(sql)
    adata = cursor.fetchone()
    while adata :
        aid = "tag_%03d" % adata[0]
        atname = adata[1]

        rsslist_array = []
        cursor2 = dbconn.cursor()
        sql2 = "select id,title,hashid,unreadcnt from rss_main where id in (select rid from tag_detail where tid=:tid) order by id"
        cursor2.execute(sql2, {"tid": adata[0]})
        bdata = cursor2.fetchone()
        while bdata :
            bid = bdata[0]
            btitle = bdata[1]
            blink = bdata[2]
            unread = bdata[3]

            rsslist_array.append({"title":btitle, "link":blink, "unread":unread})
            bdata = cursor2.fetchone()
        cursor2.close()

        rsstags_array.append({"title":atname, "link":aid, "unread":0, "sub":rsslist_array})
        adata = cursor.fetchone()

    cursor.close()
    dbconn.close()

    return rsstags_array


if __name__ == "__main__" :
    print "Content-type: application/json"
    print

    rsslist = rsslist()
    rsstags = rsstags()

    search = common.getsearch()
    # menuobj = [{"title": "訂閱", "sub": rsslist}]
    menuobj = [{"title":"星號", "link":"star", "sub":[]}, {"title":"所有項目", "sub":rsslist}]
    if (search) :
        menuobj.insert(0, {"title":"搜尋", "link":"search", "sub":[]})

    if (rsstags) :
        menuobj.append({"title":"TAG", "sub":rsstags})

    print json.dumps(menuobj)

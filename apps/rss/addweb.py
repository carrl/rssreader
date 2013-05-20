#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 從網頁抓取 rss url 相關資料, 將資料加入 rss_main 列表

import cgi
import json
import hashlib
import os
import string
import sqlite3
import sys

import getrssurl
import rss_parse

sys.path.append("../common")
import common


# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params

def webrss(weburl) :
    rssdict = {"title":None, "link":None, "description":None, "htmlurl":None, "xmlurl":None, "hashid":None}
     
    rssdict["htmlurl"] = weburl
    rssurl = getrssurl.GetRssUrl()
    rssurl.loadurl(weburl)
    rssurl = rssurl.rssurl
     
    if rssurl :
        rssdict["xmlurl"] = rssurl
        rssdict["hashid"] = hashlib.sha1(string.strip(rssurl)).hexdigest()
        rss = rss_parse.RssParse()
        rss.loadurl(rssurl)
        if (rss.first_tag == "rss") :
            for i in rss.get_atom("rss.channel") :
                for j in i :
                    if j.has_key("title") :
                        rssdict["title"] = j["title"]["c"].decode("utf-8")
                    if j.has_key("link") :
                        rssdict["link"] = j["link"]["c"]
                    if j.has_key("description") :
                        rssdict["description"] = j["description"]["c"].decode("utf-8")
        elif (rss.first_tag == "feed") :
            for i in rss.get_atom("feed") :
                for j in i :
                    if j.has_key("title") :
                        rssdict["title"] = j["title"]["c"].decode("utf-8")
                    if j.has_key("link") :
                        rssdict["link"] = j["link"]["p"]["href"]
                    if j.has_key("subtitle") :
                        rssdict["description"] = j["subtitle"]["c"].decode("utf-8")
             
        return rssdict


if __name__ == "__main__" :
    result = { "result":None, "result2":None, "message":None, "hashid":None }
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    url = params["weburl"]

    if (url != "") :
        rssdict = webrss(url)
     
        if (rssdict and rssdict["title"]) :
            dbname = common.getdbname()
            if (dbname and os.path.exists(dbname)) :
                conn = sqlite3.connect(dbname)
             
                cursor0 = conn.cursor()
                sql0 = "select xmlurl from rss_main where xmlurl=:xmlurl"
                cursor0.execute(sql0, {'xmlurl': rssdict["xmlurl"]})
             
                adata = cursor0.fetchone()
                if adata :
                    result["result2"] = "update"
                    result["message"] = "[update]:" + "(" + rssdict["htmlurl"] + ")" + rssdict["title"].encode("utf-8")
                    result["hashid"] = rssdict["hashid"]
                    cursor = conn.cursor()
                    sql = "update rss_main set title=:title,link=:link,description=:description where xmlurl=:xmlurl"
                    cursor.execute(sql, rssdict)
                    conn.commit()
                    cursor.close()
                else :
                    result["result2"] = "insert"
                    result["message"] = "[insert]:" + "(" + rssdict["htmlurl"] + ")" + rssdict["title"].encode("utf-8")
                    result["hashid"] = rssdict["hashid"]
                    cursor = conn.cursor()
                    sql = "insert into rss_main(title,link,description,htmlurl,xmlurl,hashid) values(:title,:link,:description,:htmlurl,:xmlurl,:hashid)"
                    cursor.execute(sql, rssdict)
                    conn.commit()
                    cursor.close()
             
                cursor.close()
                conn.close()

                result["result"] = "ok"
            else :
                result["result"] = "nook"
                result["message"] = "Can't get dbname"
        else :
            result["result"] = "nook"
            result["message"] = "Can't find RSS url"
    else :
        result["result"] = "nook"
        result["message"] = "No web url"

    print "Content-type: application/json"
    print

    print json.dumps(result)

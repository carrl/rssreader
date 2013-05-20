#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 顯示 rss 明細

import cgi
import string
import sqlite3
import sys
import json

sys.path.append("../common")
import common


# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params

def content(ahtml) :
    """ 將 &lt; 改為 <, 將 &gt; 改為 > """
    if (ahtml != None) :
        ahtml = string.replace(ahtml, "&lt;", "<")
        ahtml = string.replace(ahtml, "&gt;", ">")
        ahtml = string.replace(ahtml, "&amp;", "&")
 
    return ahtml

def del_script(ahtml) :
    """ 將 <script> .... </script> 的部份刪除 """
    apos = ahtml.find("<script")
    while (apos != -1) :
        bpos = ahtml.find("</script>", apos) + len("</script>")
        ahtml = ahtml[0:apos] + ahtml[bpos:]
        apos = ahtml.find("<script")

    return ahtml

def rssd_dict(id) :
    result = {}
    dbname = common.getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    sql = "select id,title,author,link,content from rss_detail where id=:id"
    cursor.execute(sql, {"id": id})

    adata = cursor.fetchone()
    if adata :
        result["id"] = adata[0]
        result["title"] = adata[1]
        if (adata[2] != None) :
            result["author"] = adata[2]
        else :
            result["author"] = ""
        result["link"] = adata[3]
        if (adata[4] != None) :
            result["content"] = del_script(content(adata[4]))
        else :
            result["content"] = ""

    cursor.close()
    dbconn.close()

    return result

if __name__ == "__main__" :
    params = cgiFieldStorageToDict( cgi.FieldStorage() )

    try :
        myid = params["id"]
    except :
        myid = ""

    print "Content-type: application/json"
    print

    if (myid) :
        rssdl = rssd_dict(myid)
    else :
        rssdl = {}

    print json.dumps(rssdl)

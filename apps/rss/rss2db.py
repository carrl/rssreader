#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 將 rss 資料存入 db

import os
import string
import sqlite3
import logging
import sys

import datehandle
import rss_parse

sys.path.append("../common")
import common


logfilename = common.getlogname()
if not (os.path.exists(logfilename)) :
    logfilename = "/tmp/rsslog.txt"
     
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logfilename,
                    filemode="a")

class Rss2DB :
    def __init__(self, dbname, showmsg=True) :
        self.showmsg = showmsg
        self.dbconn = sqlite3.connect(dbname)

    def __del__(self) :
        self.dbconn.close()

    def cal_unreadcnt(self, rssdict) :
        """ 重新 計算 unread 的數量, 存入 rss_main.unreadcnt 中 """
        cursor = self.dbconn.cursor()
     
        sql = "select count(0) from rss_detail where mainid=:mainid and readed<>1"
        cursor.execute(sql, {"mainid": rssdict["mainid"]})
        adata = cursor.fetchone()
        if adata :
            unread = adata[0]
        else :
            unread = 0
     
        cursor.close()
     
        cursor = self.dbconn.cursor()
        sql = "update rss_main set unreadcnt=:unread where id=:id"
        cursor.execute(sql, {"id": rssdict["mainid"], "unread":unread})
        self.dbconn.commit()
        cursor.close()
     
    def save2db(self, rssdict) :
        """ 將 rss 資料存入 db """
        cursor0 = self.dbconn.cursor()
        sql0 = "select rssid,pubdate,updated from rss_detail where rssid=:rssid"
        cursor0.execute(sql0, {"rssid": rssdict["rssid"]})
     
        adata = cursor0.fetchone()
        if adata :
            pubdate = adata[1]
            updated = adata[2]
            if (pubdate and (pubdate < rssdict["pubdate"])) or (updated and (updated < rssdict["updated"])) :
                cursor = self.dbconn.cursor()
                sql = "update rss_detail set title=:title,link=:link,content=:content,author=:author,pubdate=:pubdate,updated=:updated where rssid=:rssid"
                if (self.showmsg) :
                    print "[update]:", rssdict["title"].encode("utf-8")
                cursor.execute(sql, rssdict)
     
                self.dbconn.commit()
                cursor.close()
        else :
            cursor = self.dbconn.cursor()
            sql = "insert into rss_detail(mainid,rssid,title,link,content,author,pubdate,updated) values(:mainid, :rssid, :title, :link, :content, :author, :pubdate, :updated)"
            if (self.showmsg) :
                print "[insert]:", rssdict["title"].encode("utf-8")
            cursor.execute(sql, rssdict)
     
            self.dbconn.commit()
            cursor.close()
     
        cursor0.close()
     
        self.cal_unreadcnt(rssdict)
     
     
    def rss2db(self, rssurl, mainid) :
        try :
            rss = rss_parse.RssParse()
            rss.loadurl(rssurl)
             
            if rss.first_tag == "rss" :
                for i in rss.get_atom("rss.channel.item") :
                    rssdetail = {"mainid":mainid, "rssid":None, "title":None, "link":None, "content":None, "author":None, "pubdate":None, "updated":None}
                    for j in i :
                        if j.has_key("guid") :
                            rssdetail["rssid"] = j["guid"]["c"]
                        if (not rssdetail["title"]) and j.has_key("title") :
                            rssdetail["title"] = j["title"]["c"].decode("utf-8")
                        if (not rssdetail["link"]) and j.has_key("link") :
                                rssdetail["link"] = j["link"]["c"]
                        if (not rssdetail["content"]) and j.has_key("description") :
                            rssdetail["content"] = j["description"]["c"].decode("utf-8")
                        if (not rssdetail["author"]) and j.has_key("author") :
                            rssdetail["author"] = j["author"]["c"].decode("utf-8")
                        if (not rssdetail["pubdate"]) and j.has_key("pubDate") :
                            rssdetail["pubdate"] = datehandle.datehandle(j["pubDate"]["c"])
                    if rssdetail["rssid"] :
                        self.save2db(rssdetail)
            elif rss.first_tag == "feed" :
                for i in rss.get_atom("feed.entry") :
                    rssdetail = {"mainid":mainid, "rssid":None, "title":None, "link":None, "content":None, "author":None, "pubdate":None, "updated":None}
                    for j in i :
                        if j.has_key("id") :
                            rssdetail["rssid"] = j["id"]["c"]
                        if (not rssdetail["title"]) and j.has_key("title") :
                            rssdetail["title"] = j["title"]["c"].decode("utf-8")
                        if (not rssdetail["link"]) and j.has_key("link") :
                            if (j["link"]["p"].has_key("rel")) :
                                # 如果參數有 rel, 要抓取 rel="alternate" 的那一筆資料
                                if (j["link"]["p"]["rel"] == "alternate") :
                                    rssdetail["link"] = j["link"]["p"]["href"]
                            else :
                                rssdetail["link"] = j["link"]["p"]["href"]
                        if (not rssdetail["content"]) and j.has_key("content") :
                            rssdetail["content"] = j["content"]["c"].decode("utf-8")
                        if (not rssdetail["author"]) and j.has_key("author") :
                            for k in j["author"]["c"] :
                                if k.has_key("name") :
                                    rssdetail["author"] = k["name"]["c"].decode("utf-8")
                        if (not rssdetail["pubdate"]) and j.has_key("published") :
                            rssdetail["pubdate"] = datehandle.datehandle2(j["published"]["c"])
                        if (not rssdetail["updated"]) and j.has_key("updated") :
                            rssdetail["updated"] = datehandle.datehandle2(j["updated"]["c"])
                    # 如果沒有 pubdate, 用 updated 取代 pubdate
                    if (rssdetail["pubdate"] == None) :
                        rssdetail["pubdate"] = rssdetail["updated"]
                    if rssdetail["rssid"] :
                        self.save2db(rssdetail)
     
            del rss
        except:
            if (self.showmsg) :
                print "ERROR !!!"
            logging.info("Error: " + rssurl)
     
    def updateall(self) :
        """ 更新 db.rss_main 中所有 xmlurl 的 RSS 資料 """
        cursor = self.dbconn.cursor()
        sql = "select id,title,xmlurl from rss_main"
        cursor.execute(sql)
         
        alldata = cursor.fetchall()
        for adata in alldata:
            aid = adata[0]
            atitle = adata[1].encode("utf-8")
            axmlurl = adata[2]
            if (self.showmsg) :
                print "===== %03d [%s] =====" % (aid, atitle)
            self.rss2db(axmlurl, aid)
         
        cursor.close()

     
    def updatesingle(self, hashid) :
        """ 更新 db.rss_main 中某個 xmlurl 的 RSS 資料 """
        cursor = self.dbconn.cursor()
        sql = "select id,title,xmlurl from rss_main where hashid=:hashid"
        cursor.execute(sql, {"hashid": hashid})
         
        alldata = cursor.fetchall()
        for adata in alldata:
            aid = adata[0]
            atitle = adata[1].encode("utf-8")
            axmlurl = adata[2]
            if (self.showmsg) :
                print "===== %03d [%s] =====" % (aid, atitle)
            self.rss2db(axmlurl, aid)
         
        cursor.close()

if __name__ == "__main__" :
    dbname = common.getdbname()
    if (dbname and os.path.exists(dbname)) :
        rss2db = Rss2DB(dbname)
        if (len(sys.argv) > 1) :
            rss2db.updatesingle(sys.argv[1])
        else :
            rss2db.updateall()
    else :
        print "Can't get db !!"

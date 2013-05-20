#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 從網頁資料中取得 rss url

import string
import urllib
import urllib2
import urlparse

class GetRssUrl :
    def __init__(self) :
        self.rssurl = ""

    def loadfile(self, filename) :
        try :
            inf = open(filename, "r")
            ahtml = inf.read()
            inf.close()
     
            self.rssurl = self.getrssurl(ahtml)
        except :
            self.rssurl = ""

    def loadurl(self, aurl) :
        try :
            my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"}
            req = urllib2.Request(aurl, headers=my_headers)

            urlf = urllib2.urlopen(req, timeout=3)
            ahtml = urlf.read()
            urlf.close()
     
            my_rssurl = self.getrssurl(ahtml)
            if (my_rssurl[0] == "/") :
                self.rssurl = urlparse.urljoin(aurl, my_rssurl)
            else :
                self.rssurl = self.getrssurl(ahtml)
        except :
            self.rssurl = ""

    def get_params(self, params) :
        """ 分析 prarms, 要注意到類似 aa="bb cc dd" 之類的情況 """
        params = string.strip(params)
        params = string.replace(params, "\n", "")
        result = {}
        if (params[-1] == "/") :
            params = string.strip(params[:-1])
     
        while not (params == "") :
            apos = params.find("=")
            if (params[apos+1] in ["'", "\""]) :
                endchar = params[apos+1]
                bpos = params.find(endchar, apos+2)
                key = string.strip(params[:apos])
                value = string.strip(params[apos+2: bpos])
            else :
                bpos = params.find(" ")
                key = string.strip(params[:apos])
                value = string.strip(params[apos+1: bpos])
            result[key] = value
            params = string.strip(params[bpos+1:])
     
        return result
     
    def getrssurl(self, astr) :
        """ 從網頁資料中取得 rss url """
        result = ""
        atomlink = ""
     
        apos = astr.find("<link")
        while (apos != -1) :
            astr = astr[apos:]
     
            # 找出目前 tag 的結尾 > 位置
            my_tag = "link"
            bpos = astr.find(">", len(my_tag)+1)
            while (len(astr[0:bpos].split("\"")) % 2) == 0 :
                bpos = astr.find(">", bpos+1)
     
            aparams = astr[len(my_tag)+2:bpos]
     
            params = self.get_params(aparams)
     
            # 抓取第一筆 rss 資料
            if (params.has_key("type")) and ("rss+xml" in params["type"]) :
                result = params["href"]
                break

            # 抓取第一筆 atom 資料
            if (atomlink == "") :
                if ((params.has_key("type")) and ("atom+xml" in params["type"])) :
                    atomlink = params["href"]
     
            apos = astr.find("<link", bpos+1)

        # 當 rss 沒有資料時才採用 atom 資料
        if (result == "") :
            result = atomlink
     
        return result

if __name__ == "__main__" :
    url = "http://googleblog.blogspot.tw/"

    rss = GetRssUrl()
    rss.loadurl(url)
    print rss.rssurl
    del rss

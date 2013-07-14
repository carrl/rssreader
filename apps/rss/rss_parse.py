#! /usr/bin/env python
#-*- coding:utf-8 -*-

import string
import time
import datehandle

class RssParse:
    def __init__(self) :
        self.axml = ""
        self.encoding = ""
        self.arss = ""
        self.first_tag = ""

    def loadfile(self ,filename) :
        """ 從 檔案 讀取資料 """
        inf = open(filename, "r")
        self.axml = inf.read()
        inf.close()

        self.encoding = self.get_encoding(self.axml)
        self.axml = self.to_utf8(self.axml)

        self.first_tag = self.find_tag(self.axml)

        end_tag = "</" + self.first_tag + ">"
        if (self.axml.find(end_tag) != -1) : # 有發現結束的 tag (ex:</rss> or </feed>) 才執行 self.get_content
            (before, self.arss, after) = self.get_content(self.axml, self.first_tag)
            self.rssdict = self.parse(self.arss)
        else :
            self.rssdict = []

    def loadurl(self, url) :
        """ 從 URL 讀取資料 """
        import urllib2
        try :
            my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"}
            req = urllib2.Request(url, headers=my_headers)

            urlf = urllib2.urlopen(req, timeout=5)
            self.axml = urlf.read()
            urlf.close()
            self.encoding = self.get_encoding(self.axml)
            self.axml = self.to_utf8(self.axml)
        except :
            self.axml = ""

        self.first_tag = self.find_tag(self.axml)

        end_tag = "</" + self.first_tag + ">"
        if (self.axml.find(end_tag) != -1) : # 有發現結束的 tag (ex:</rss> or </feed>) 才執行 self.get_content
            (before, self.arss, after) = self.get_content(self.axml, self.first_tag)
            self.rssdict = self.parse(self.arss)
        else :
            self.rssdict = []

    def get_encoding(self, xml) :
        """ 取得 <?xml ... ?> 中 encoding的值 """
        if (xml.find("<?xml") != -1) :
            apos = xml.find("<?xml")+len("<?xml")
            bpos = xml.find("?>")
            xmlstr = xml[apos:bpos].strip()
            my_encoding = self.get_params(xmlstr)["encoding"]
        else :
            xmlstr = ""
            my_encoding = ""
        
	if my_encoding == "big5" :
	    my_encoding = "cp950"

        return my_encoding

    def to_utf8(self, str) :
        """ 根據 self.encoding encode 到 utf-8 """
        if ((string.upper(self.encoding) != "UTF-8") and (string.upper(self.encoding) != "")) :
            return str.decode(self.encoding).encode("utf-8")
        else :
            return str

    def findapos(self, xml, tag) :
        """ 找到 xml裡 開始的 tag 位置 """
        atag = "<" + tag  # tag 開始字串
        apos = xml.find(atag)

        return apos

    def findbpos(self, xml, tag) :
        """ 找到 xml 裡 結束的 tag 位置 """
        atag = "<" + tag  # tag 開始字串
        btag = "</" + tag + ">" # tag 結束字串
        apos = xml.find(atag)

        cnt = 0
        beginpos = apos+len(atag)

        while True :
            atype = 1           # 1: </tag>, 2: />
            aa = xml.find("<", beginpos)
            bb = xml.find("/>", beginpos)
            if (aa == -1) : aa = 99999999
            if (bb == -1) : bb = 99999999
            if (aa < bb) :
                atype = 1                          # 發現 "</tag>"
                if (xml[aa+1:aa+8] == "![CDATA") : # 避過 <![CDATA[....]]> 的 內容
                    beginpos = xml.find("]]>",beginpos) + len("]]>")
                else :
                    if (xml[aa+1] == "/") :
                        cnt -= 1
                    else :
                        cnt += 1
                    if (cnt >= 0) :
                        beginpos = aa + 1
            elif (bb != -1) :   # 發現 "/>"
                atype = 2
                cnt -= 1
                if (cnt >= 0) :
                    beginpos = bb + 1
            if (cnt < 0) :
                break

        if (atype == 1) :
            bpos = xml.find(btag, beginpos)
        else :
            btag = "/>"
            bpos = xml.find(btag, beginpos)

        result = (bpos, len(btag))
        return result

    def get_content(self, xml, tag) :
        """ 取得 xml 裡 tag 的內容 """

        apos = self.findapos(xml, tag)
        (bpos, bsize) = self.findbpos(xml, tag)
        before = xml[0:apos]
        axml = xml[apos:bpos+bsize]
        after = xml[bpos+bsize:]

        return (before, axml, after)

    def show_content(self, tag) :
        """ 顯示 xml 裡 tag 的內容 """

        apos = self.findapos(self.arss, tag)
        (bpos, bsize) = self.findbpos(self.arss, tag)
        axml = self.arss[apos:bpos+bsize]

        print axml

    def find_tag(self, astr) :
        """ 如果 astr 裡還有 '<' , 傳回 tag, 否則傳回 '' """
        astr = string.replace(astr, "\n", "")

        apos = astr.find("<")
        while (astr[apos+1:apos+8] == "![CDATA") :
            apos = astr.find("]]>", apos+8) + 1
        while (astr[apos+1] == "?" or astr[apos+1] == "!") :
            apos = astr.find("<", apos+1)

        if (apos != -1) :
            my_pos1 = astr.find(" ", apos)
            my_pos2 = astr.find(">", apos)
            if (my_pos1 == -1) : my_pos1 = 99999999
            if (my_pos2 == -1) : my_pos2 = 99999999
            my_pos = min(my_pos1, my_pos2)
            my_tag = astr[apos+1:my_pos]
        else :
            my_tag = ""

        return my_tag

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

    def parse(self, xml) :
        result = []
        if xml :
            my_tag = self.find_tag(xml)
            if my_tag :
                result1 = []
                (before, axml, after) = self.get_content(xml, my_tag)

                if (before) :
                    result1.extend(xml)

                # 找出目前 tag 的結尾 > 位置
                apos = axml.find(">", len(my_tag)+1)
                while (len(axml[0:apos].split("\"")) % 2) == 0 :
                    apos = axml.find(">", apos+1)

                aparams = axml[len(my_tag)+2:apos]
                if (aparams) :
                    params_dict = self.get_params(aparams)
                else :
                    params_dict = None

                bpos = axml.rfind("</")
                if (bpos == -1) :
                    bpos = axml.rfind("/>")
                    content = ""
                else :
                    content = axml[apos+1:bpos]

                if content :
                    if (params_dict) :
                        result1.extend([{my_tag: {"c": self.parse(string.strip(content)), "p": params_dict}}])
                    else :
                        result1.extend([{my_tag: {"c": self.parse(string.strip(content))}}])
                else :
                    if (params_dict) :
                        result1.extend([{my_tag: {"c": "", "p": params_dict}}])
                    else :
                        result1.extend([{my_tag: {"c": ""}}])

                if (after) :
                    result1.extend(self.parse(string.strip(after)))

                result.extend(result1)
            else :
                if (string.strip(xml)) :
                    xml = string.strip(xml)
                    if (xml[0:8] == "<![CDATA") and (xml[-3:] == "]]>") :
                        xml = xml[9:-3]
                    return xml
                else :
                    return ""

            return result

    def get_atom(self, atom) :
        """ 從 轉成的 dict 取出資料 """
        result = []

        rssdict = self.rssdict
        all_atoms = string.split(atom, ".")
        for i in all_atoms :
            new_rssdict = []
            for j in rssdict :
                if j.has_key(i) :
                    if (i == all_atoms[-1]) :
                        new_rssdict.append(j[i]["c"])
                    else :
                        new_rssdict.extend(j[i]["c"])
            rssdict = new_rssdict

        return rssdict

    def show_allitems(self) :
        """ 顯示所有 rss item """
        if (self.first_tag == "rss") : # rss2full.xsl
            for i in self.get_atom("rss.channel.title") :
                print "[title]:", i

            for i in self.get_atom("rss.channel.description") :
                print "[description]:", i

            for i in self.get_atom("rss.channel.link") :
                print "[link]:", i

            print "=================================="

            for i in self.get_atom("rss.channel.item") :
                for j in i :
                    if j.has_key("rssid") :
                        print "[rssid]:", j["rssid"]["c"]
                    if j.has_key("title") :
                        print "[title]:", j["title"]["c"]
                    if j.has_key("link") :
                        print "[link]:", j["link"]["c"]
                    if j.has_key("author") :
                        print "[author]:", j["author"]["c"]
                    if j.has_key("guid") :
                        # print "[guid]p:", j["guid"]["p"]
                        print "[guid]c:", j["guid"]["c"]
                    if j.has_key("pubDate") :
                        print "[pubDate]:", time.gmtime(datehandle.datehandle(j["pubDate"]["c"]))
                    if j.has_key("atom:updated") :
                        print "[atom:updated]:", time.gmtime(datehandle.datehandle2(j["atom:updated"]["c"]))
                    if j.has_key("category") :
                        print "[category]:", j["category"]["c"]

                print "============="

        elif (self.first_tag == "feed") : # atom10full.xsl
            for i in self.get_atom("feed.title") :
                print "[title]:", i

            for i in self.get_atom("feed.subtitle") :
                print "[subtitle]:", i

            for i in self.get_atom("feed") :
                for j in i :
                    if j.has_key("link") :
                        print "[link]:", j["link"]["p"]["href"]

            print "=================================="

            for i in self.get_atom("feed.entry") :
                for j in i :
                    if j.has_key("rssid") :
                        print "[rssid]:", j["rssid"]["c"]
                    if j.has_key("title") :
                        print "[title]:", j["title"]["c"]
                    if j.has_key("link") :
                        print "[link.href]:", j["link"]["p"]["href"]
                    if j.has_key("author") :
                        print "[author]:", j["author"]["c"]
                    if j.has_key("id") :
                        print "[id]:", j["id"]["c"]
                    if j.has_key("published") :
                        print "[published]:", j["published"]["c"]
                    if j.has_key("updated") :
                        print "[updated]:", time.gmtime(datehandle.datehandle2(j["updated"]["c"]))

                print "============="

        else :
            print "unknown rss format"
            print self.get_atom("opml.head.title")[0]
            print "=================================="
            for i in self.get_atom("opml.body") :
                for j in i :
                    if j.has_key("outline") :
                        print j["outline"]["p"]["text"]
                        for k in j["outline"]["c"] :
                            if k.has_key("outline") :
                                print "  ", k["outline"]["p"]["text"],
                                print "(", k["outline"]["p"]["xmlUrl"], ")"


if __name__ == "__main__" :
    rss = RssParse()

    rss.loadurl("http://googleblog.blogspot.com/feeds/posts/default?alt=rss")

    rss.show_allitems()
    del rss

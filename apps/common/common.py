#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 公用程式

import sqlite3
import yaml

class Conf :
    def __init__(self) :
        self.confs = {"db":None, "log":None, "search":None}
        try :
            yamlf = open("../../config/conf.yaml", "r")
            yamlobj = yaml.load(yamlf)
            for conf in self.confs :
                if yamlobj[0].has_key(conf) :
                    self.confs[conf] = yamlobj[0][conf]
            yamlf.close()
        except :
            pass

    def dbname(self) :
        return self.confs["db"]

    def logname(self) :
        return self.confs["log"]

    def search(self) :
        return self.confs["search"]


def getdbname() :
    """ 從 config/conf.yaml 取得 db 路徑 """
    conf = Conf();
    return conf.dbname()

def getlogname() :
    """ 從 config/conf.yaml 取得 log 檔案路徑 """
    conf = Conf();
    return conf.logname()

def getsearch() :
    """ 從 config/conf.yaml 取得 search 的值 """
    conf = Conf();
    return conf.search()

def checkfield(fieldname, tablename) :
    """ 檢查 tablename 是否有欄位 fieldname """
    dbname = getdbname()

    dbconn = sqlite3.connect(dbname)
    cursor = dbconn.cursor()

    fieldnames = []
    sql = "pragma table_info('" + tablename + "');"
    cursor.execute(sql)
    adata = cursor.fetchone()
    while adata :
        # print adata[1]
        fieldnames.append(adata[1])
        adata = cursor.fetchone()

    cursor.close()
    dbconn.close()

    return (fieldname in fieldnames)


if __name__ == "__main__" :
    print getdbname()
    print getlogname()
    print getsearch()

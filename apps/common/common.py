#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 公用程式

import sqlite3
import yaml

def getdbname() :
    """ 從 config/conf.yaml 取得 db 路徑 """
    try :
        yamlf = open("../../config/conf.yaml", "r")

        yamlobj = yaml.load(yamlf)

        yamlf.close()

        return yamlobj[0]["db"]
    except :
        return ""

def getlogname() :
    """ 從 config/conf.yaml 取得 log 檔案路徑 """
    try :
        yamlf = open("../../config/conf.yaml", "r")

        yamlobj = yaml.load(yamlf)

        yamlf.close()

        return yamlobj[0]["log"]
    except :
        return ""

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

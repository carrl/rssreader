#! /usr/bin/env python
#-*- coding:utf-8 -*-
# 公用程式

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


if __name__ == "__main__" :
    print getdbname()
    print getlogname()

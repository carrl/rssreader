#! /usr/bin/env python
#-*- coding: utf-8 -*-
# 將 config 裡的 yaml 檔轉成 json 輸出

import cgi
import os
import yaml
import json

# 將傳入的參數，存成 辭典集
def cgiFieldStorageToDict( fieldStorage ):
    params = {}
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
    return params

params = cgiFieldStorageToDict( cgi.FieldStorage() )

try :
    conf_file = params["conf"]
    conf_file = "../config/" +conf_file + ".yaml"
except :
    conf_file = ""

print "Content-type: application/json"
print

if (conf_file != "" and  os.path.exists(conf_file)) :
    conf = open(conf_file, "r")

    yamlobj = yaml.load(conf)

    conf.close()

    jsonobj = json.dumps(yamlobj)

    print jsonobj

#! /usr/bin/env python
#-*- coding:utf-8 -*-
# setup.py

import os
import shutil


# 建立 config 目錄
if not os.path.exists("../config") :
    os.mkdir("../config")

if not os.path.exists("../config/conf.yaml") :
    shutil.copy("conf.yaml", "../config/conf.yaml")

# 建立 db 目錄
if not os.path.exists("../db") :
    os.mkdir("../db")

if not os.path.exists("../db/rssdata.db") :
    shutil.copy("rssdata.db", "../db/rssdata.db")

if not os.path.exists("../db/rsslog.txt") :
    shutil.copy("rsslog.txt", "../db/rsslog.txt")

# 變更 db/* 權限, 讓所有人可以讀寫
os.chmod("../db", 0777)
os.chmod("../db/rssdata.db", 0666)
os.chmod("../db/rsslog.txt", 0666)

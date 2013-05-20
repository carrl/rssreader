RSS reader
==========

開發來自己使用的 RSS reader

Screenshot
----------
![圖片1](https://github.com/carrl/rssreader/raw/master/screenshot/screenshot1.png)

我的環境
--------

* ubuntu
* apache
* python 2.X
* sqlite3
	
安裝
----
* git clone https://github.com/carrl/rssreader.git
* cd rssreader
* cd install
* python setup.py

apache 設定
-----------
加上**設定值**

	AddHandler cgi-script .py

及

	<Directory /PATH/rssreader>
	  Options +ExecCGI
	</Directory>

然後 **restart apache**

更新資料
--------
	設定 cron 來執行 apps/rss/rss2db.py, 固定一段時間更新 rss 資料
	ex:
	30 */2 * * * /PATH/apps/rss/rss2db.py
	固定每兩個小時就執行一次

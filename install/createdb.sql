create table if not exists rss_main (
	id integer primary key autoincrement,
	title varchar,
	link varchar,
	description varchar,
	htmlurl varchar,
	xmlurl varchar,
	updated date,
	hashid varchar,
	unreadcnt integer default 0
);

create table if not exists rss_detail (
	id integer primary key autoincrement,
	mainid integer,
	rssid varchar,
	title varchar,
	link varchar,
	content text,
	author varchar,
	pubdate date,
	updated date,
	readed boolean default 0,
	star boolean default 0
);

CREATE TABLE post (
	id INTEGER PRIMARY KEY,
	title TEXT,
	published_date DATE,
	author TEXT,
	content TEXT,
	permalink_url TEXT
);

CREATE TABLE user (
	id INTEGER PRIMARY KEY,
	username TEXT,
    password TEXT
);
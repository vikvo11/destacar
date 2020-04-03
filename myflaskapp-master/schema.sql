CREATE TABLE IF NOT EXISTS users(name text, email string, username string, password string);
CREATE TABLE IF NOT EXISTS articles_v(id INTEGER PRIMARY KEY,title text, body string, author string);
CREATE TABLE IF NOT EXISTS template(id INTEGER PRIMARY KEY,name text, body string, param string, link string);
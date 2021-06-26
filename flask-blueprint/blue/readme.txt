Export2SQLCE.exe "Data Source=(local);Initial Catalog=gravi_angelok;Integrated Security=True" wp_posts.sql sqlite


INSERT INTO articles(title,body,author,data) VALUES('New_test','New_test','New_test',2021-07-15);

CREATE TABLE IF NOT EXISTS articles_new(name text, email string, username string, password string)

delete from articles;


sqlite3 db.name
.tables
.headers on

select * from articles;

sqlite> .read wp_posts.sql
Or:

cat db.sql | sqlite3 database.db
Also, your SQL is invalid - you need ; on the end of your statements:

create table server(name varchar(50),ipaddress varchar(15),id init);
create table client(name varchar(50),ipaddress varchar(15),id init);



SELECT Concat(`post_author`, ' (', `post_status`, ')') FROM `wp_posts` where id=32

select concat('The Year is ', post_author,'Oops ', post_status ), concat('The month is ', post_status) FROM `wp_posts` where id=32

select concat('INSERT INTO articles(title,body,author,data) VALUES(',post_title,',',post_content,',',post_author,',',post_date,');') FROM `wp_posts` where id=32

select concat('INSERT INTO articles(title,body,author,data) VALUES(',"'",post_title,"'",',',"'",post_content,"'",',',"'",post_author,"'",',',"'",post_date,"'",');') FROM `wp_posts` where id=30 or id=32

#####
select concat('INSERT INTO articles(title,body,author,data) VALUES

(',"'",post_title,"'",',',"'",post_content,"'",',',"'",post_author,"'",',',"'",post_date,"'",');') FROM `wp_posts` where

post_status="publish" and id > 500 and id < 1000 ORDER by post_date
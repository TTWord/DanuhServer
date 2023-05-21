drop table user;
drop table book;
drop table word;
drop table certification;
drop table file;

create table user(
    id INT PRIMARY KEY auto_increment,
    username VARCHAR(100),
    password VARCHAR(100),
    nickname VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    file_id INT,
)

create table book(
    id INT PRIMARY KEY auto_increment,
    user_id INT,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

create table word(
    id INT PRIMARY KEY auto_increment,
    book_id INT,
    word VARCHAR(100),
    mean VARCHAR(100),
    is_memorized BOOLEAN not null default 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

create table certification(
    id INT PRIMARY KEY auto_increment,
    cert_type VARCHAR(100),
    cert_key VARCHAR(100),
    cert_code VARCHAR(100),
    expired_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

create table file(
    id INT PRIMARY KEY auto_increment,
    file_path VARCHAR(100)
)
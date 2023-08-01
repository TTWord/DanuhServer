drop table user;
drop table book;
drop table word;
drop table certification;
drop table file;
drop table share;
drop table commend;
drop table book_share;

create table user(
    id INT PRIMARY KEY auto_increment,
    username VARCHAR(100) unique,
    password VARCHAR(100),
    nickname VARCHAR(100),
    login_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table book(
    id INT PRIMARY KEY auto_increment,
    user_id INT,
    name VARCHAR(100),
    is_downloaded BOOLEAN default 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

create table recommend(
    id INT PRIMARY KEY auto_increment,
    like_user_id INT default 0,
    book_id INT default 0,
    FOREIGN KEY(like_user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY(book_id) REFERENCES book(id) ON DELETE CASCADE
);

create table share(
    id INT PRIMARY KEY auto_increment,
    book_id INT,
    is_shared BOOLEAN default 1,
    comment VARCHAR(100),
    checked INT default 0,
    downloaded INT default 0,
    recommended INT default 0,
    FOREIGN KEY(book_id) REFERENCES book(id) ON DELETE CASCADE
);

create table book_share(
    id INT PRIMARY KEY auto_increment,
    book_id INT default 0,
    share_id INT default 0,
    FOREIGN KEY(book_id) REFERENCES book(id) ON DELETE CASCADE,
    FOREIGN KEY(share_id) REFERENCES share(id) ON DELETE CASCADE
);

create table word(
    id INT PRIMARY KEY auto_increment,
    book_id INT,
    word VARCHAR(100),
    mean VARCHAR(100),
    is_memorized BOOLEAN not null default 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(book_id) REFERENCES book(id) ON DELETE CASCADE
);

create table certification(
    id INT PRIMARY KEY auto_increment,
    user_id INT,
    cert_type VARCHAR(100),
    cert_key VARCHAR(100),
    cert_code VARCHAR(100),
    expired_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

create table file(
    id INT PRIMARY KEY auto_increment,
    user_id INT,
    file_path VARCHAR(100),
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);
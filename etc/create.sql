drop table user;
drop table book;
drop table word;
drop table certification;
drop table file;

create table user(
    id INT PRIMARY KEY auto_increment,
    username VARCHAR(100) unique,
    password VARCHAR(100),
    nickname VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table book(
    id INT PRIMARY KEY auto_increment,
    user_id INT,
    name VARCHAR(100),
    is_downloaded BOOLEAN default 0,
    is_shared BOOLEAN default 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

create table share(
    id INT PRIMARY KEY auto_increment,
    book_id INT,
    comment VARCHAR(100),
    checked INT default 0,
    downloaded INT default 0,
    FOREIGN KEY(book_id) REFERENCES book(id) ON DELETE CASCADE
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
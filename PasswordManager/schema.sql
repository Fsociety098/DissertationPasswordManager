DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS password;
DROP TABLE IF EXISTS passwordinfo;
DROP TABLE IF EXISTS categoryPassword;
DROP TABLE IF EXISTS category;




CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT,
    userID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES user (id)
);
CREATE TABLE categoryPassword (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryID INTEGER,
    passwordID INTEGER,
    FOREIGN KEY (categoryID) REFERENCES category(id),
    FOREIGN KEY (passwordID) REFERENCES password (id)
);
CREATE TABLE password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passwordinfoID INTEGER,
    userID INTEGER,
    password TEXT,
    FOREIGN KEY (passwordinfoID) REFERENCES passwordinfo (id),
    FOREIGN KEY (userID) REFERENCES  user(id)
);

CREATE TABLE passwordinfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    titlename TEXT,
    passwordid INTEGER,
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (passwordid) REFERENCES password (id)
);

CREATE TABLE user(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  passwordid INTEGER,
  fName Text NOT NULL,
  userEmail TEXT UNIQUE NOT NULL,
  secureKey TEXT NOT NULL,
  password TEXT NOT NULL,
  created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (passwordid) REFERENCES password (id)
);

insert into category (categoryName, userID)values ('Login','0');
insert into category (categoryName, userID)values ('Other','0');
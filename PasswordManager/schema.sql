DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS password;
DROP TABLE IF EXISTS passwordinfo;
DROP TABLE IF EXISTS linktable;
DROP TABLE IF EXISTS category;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fName Text NOT NULL,
  userEmail TEXT UNIQUE NOT NULL,
  secureKey TEXT NOT NULL,
  password TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
CREATE TABLE linktable(
    id integer PRIMARY KEY AUTOINCREMENT,
    passwordid INTEGER NOT NULL,
    categoryid INTEGER NOT NULL,
    passwordinfoid INTEGER NOT NULL,
    FOREIGN KEY (passwordid) REFERENCES password (id),
    FOREIGN KEY (categoryid) REFERENCES category (id),
    FOREIGN KEY (passwordinfoid) REFERENCES passwordinfo (id)
);
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT,
    userID REFERENCES linktable (id),
    FOREIGN KEY (id) REFERENCES linktable (id)
);

CREATE TABLE password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT,
    FOREIGN KEY (id) REFERENCES linktable (id)
);

CREATE TABLE passwordinfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    titlename TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES linktable (id)
);

insert into category (categoryName, userID)values ('Login','0');
insert into category (categoryName, userID)values ('Other','0');
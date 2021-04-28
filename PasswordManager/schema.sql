DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS passwordinfo;
DROP TABLE IF EXISTS userPass;
DROP TABLE IF EXISTS category;



CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT,
    userID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES user (id) ON UPDATE CASCADE
);


CREATE TABLE passwordinfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    titlename TEXT,
    password TEXT,
    category_id INTEGER,
    created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastmodified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category (id) ON UPDATE CASCADE
);

CREATE TABLE user(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  passwordid INTEGER,
  fName Text NOT NULL,
  userEmail TEXT UNIQUE NOT NULL,
  secureKey TEXT NOT NULL,
  password TEXT NOT NULL,
  created_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (passwordid) REFERENCES passwordinfo (id) ON UPDATE CASCADE
);

CREATE TABLE userPass(
    id INTEGER PRIMARY KEY NOT NULL,
    userid INTEGER,
    passid INTEGER,
    FOREIGN KEY (userid) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY (passid) REFERENCES passwordinfo(id) ON UPDATE CASCADE
);

insert into category (categoryName, userID)values ('Login','0');
insert into category (categoryName, userID)values ('Other','0');
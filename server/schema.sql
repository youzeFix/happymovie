DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS movies;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  usertype INTEGER NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_name TEXT NOT NULL,
    movie_runtime INTEGER NOT NULL,
    movie_rating REAL NOT NULL,
    movie_likability INTEGER,
    have_seen INTEGER,
    origin TEXT,
    create_time TIMESTAMP NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP,'localtime')),
    FOREIGN KEY (creator_id) REFERENCES user (id)
);
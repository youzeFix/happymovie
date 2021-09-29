DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_name TEXT NOT NULL,
    movie_runtime INTEGER NOT NULL,
    movie_rating REAL NOT NULL,
    movie_likability INTEGER,
    have_seen INTEGER,
    origin TEXT,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
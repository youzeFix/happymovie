import sqlite3
import time
from typing import Tuple, List

db_name = "my_movies.db"

CREATE_MOVIE_TABLE_STATEMENT = '''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_name TEXT NOT NULL,
    movie_runtime INT NOT NULL,
    movie_rating REAL,
    movie_likability INT,
    have_seen INT,
    origin TEXT,
    create_time INT NOT NULL
)
'''

db = sqlite3.connect(db_name)

db.execute(CREATE_MOVIE_TABLE_STATEMENT)

def insert_movie(movie_name:str, movie_runtime:int, movie_rating:float, movie_likability:int=1, have_seen:int=0, origin:str=None):
    INSERT_MOVIE_STATEMENT = '''
    INSERT INTO movies (movie_name,movie_runtime,movie_rating,movie_likability,have_seen,origin,create_time) VALUES (?,?,?,?,?,?,?) 
    '''

    create_time = int(time.time())

    sql_params = (movie_name, movie_runtime, movie_rating, movie_likability, have_seen, origin, create_time)
    with db:
        db.execute(INSERT_MOVIE_STATEMENT, sql_params)

def get_all_movies() -> List[Tuple]:
    QUERY_ALL_MOVIE_STATEMENT = '''
    SELECT * FROM movies
    '''
    res = []
    for row in db.execute(QUERY_ALL_MOVIE_STATEMENT):
        res.append(tuple(row))

    return res

def remove_movie(id):
    REMOVE_MOVIE_STATEMENT = '''
    DELETE FROM movies WHERE id = ?
    '''
    db.execute(REMOVE_MOVIE_STATEMENT, (id,))

def update_movie(id:int, movie_rating:float=None, movie_likability:int=None, have_seen:int=None, origin:str=None):
    params = locals()
    del params['id']
    tmp_l = [f'{k}={v}' for k,v in params.items() if v is not None]

    UPDATE_MOVIE_STATEMENT = f'''
    UPDATE movies SET {','.join(tmp_l)} WHERE id = ?
    '''
    print(UPDATE_MOVIE_STATEMENT)

    db.execute(UPDATE_MOVIE_STATEMENT, (id,))


if __name__ == "__main__":
    
    # row = db.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name =?', ('movies',))
    # print(row.fetchone())
    pass
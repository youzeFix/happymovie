import sqlite3

import click
from flask import current_app, g
from flask.app import Flask
from flask.cli import with_appcontext
import time
from typing import Tuple, List

def get_db():
    if 'db' not in g:
        g.db = db()
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db._db.executescript(f.read().decode('utf8'))

class db:

    def __init__(self) -> None:
        self._db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    def close(self):
        self._db.close()

    def insert_movie(self, movie_name:str, movie_runtime:int, movie_rating:float, movie_likability:int=1, have_seen:int=0, origin:str=None):
        INSERT_MOVIE_STATEMENT = '''
        INSERT INTO movies (movie_name,movie_runtime,movie_rating,movie_likability,have_seen,origin) VALUES (?,?,?,?,?,?) 
        '''

        sql_params = (movie_name, movie_runtime, movie_rating, movie_likability, have_seen, origin)
        with self._db:
            self._db.execute(INSERT_MOVIE_STATEMENT, sql_params)

    def query_all_movies(self) -> List[Tuple]:
        QUERY_ALL_MOVIE_STATEMENT = '''
        SELECT * FROM movies
        '''
        res = []
        for row in self._db.execute(QUERY_ALL_MOVIE_STATEMENT):
            res.append(tuple(row))

        return res

    def remove_movie(self, id):
        REMOVE_MOVIE_STATEMENT = '''
        DELETE FROM movies WHERE id = ?
        '''
        self._db.execute(REMOVE_MOVIE_STATEMENT, (id,))

    def update_movie(self, id:int, movie_rating:float=None, movie_likability:int=None, have_seen:int=None, origin:str=None):
        params = locals()
        del params['id']
        tmp_l = [f'{k}={v}' for k,v in params.items() if v is not None]

        UPDATE_MOVIE_STATEMENT = f'''
        UPDATE movies SET {','.join(tmp_l)} WHERE id = ?
        '''
        print(UPDATE_MOVIE_STATEMENT)

        self._db.execute(UPDATE_MOVIE_STATEMENT, (id,))
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the databases.')

def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
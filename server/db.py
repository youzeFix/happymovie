import sqlite3

import click
from flask import current_app, g
from flask.app import Flask
from flask.cli import with_appcontext
import time
from typing import Tuple, List
import pandas
import datetime

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

    def insert_movie(self, movie_name:str, movie_runtime:int, movie_rating:float, movie_likability:int=1, have_seen:int=0, origin:str=None, create_time:datetime.datetime=None):
        loc = locals()
        del loc['self']
        sql_column = list(loc.keys())
        if create_time is None:
            sql_column.remove('create_time')
        
        INSERT_MOVIE_STATEMENT = f'''
        INSERT INTO movies ({','.join(sql_column)}) VALUES ({','.join(['?']*len(sql_column))}) 
        '''

        sql_params = ([loc[key] for key in sql_column])
        # sql_params = (movie_name, movie_runtime, movie_rating, movie_likability, have_seen, origin, create_time)
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

    def query_one_movie_by_id(self, id) -> Tuple:
        QUERY_ONE_MOVIE_STATEMENT = '''
        SELECT * FROM movies WHERE id = ?
        '''

        res = self._db.execute(QUERY_ONE_MOVIE_STATEMENT, (id,)).fetchone()

        return res

    def query_last_insert_row(self) -> Tuple:
        last_insert_row_id = self._db.execute('SELECT LAST_INSERT_ROWID()').fetchone()[0]
        print('last insert row id is', last_insert_row_id)
        return self.query_one_movie_by_id(last_insert_row_id)

    def remove_movie(self, id):
        REMOVE_MOVIE_STATEMENT = '''
        DELETE FROM movies WHERE id = ?
        '''
        with self._db:
            self._db.execute(REMOVE_MOVIE_STATEMENT, (id,))

    def update_movie(self, id:int, movie_runtime:int=None, movie_rating:float=None, movie_likability:int=None, have_seen:int=None, origin:str=None):
        params = locals()
        del params['id']
        del params['self']
        tmp_l = [f"{k}='{v}'" for k,v in params.items() if v is not None]

        UPDATE_MOVIE_STATEMENT = f'''
        UPDATE movies SET {','.join(tmp_l)} WHERE id = ?
        '''
        # print(UPDATE_MOVIE_STATEMENT, id)

        with self._db:
            self._db.execute(UPDATE_MOVIE_STATEMENT, (id,))
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the databases.')

@click.command('import-movies')
@click.option('--filename', default='movies.xlsx', help='xlsx file name to be imported')
@with_appcontext
def import_movies(filename):
    with current_app.open_resource(filename) as f:
        required_col = ['movie_name', 'movie_runtime', 'movie_rating']
        col_scope = ['movie_name', 'movie_runtime', 'movie_rating', 'movie_likability', 'have_seen', 'origin']
        excel = pandas.read_excel(f)
        cols = [col for col in excel.columns if col in col_scope]
        for col in required_col:
            if col not in cols:
                current_app.logger.error(f'there must be {col} column')
                return

        data = excel.loc[:, cols]
        db = get_db()

        cols = required_col.copy()
        cols.extend([i for i in cols if i not in required_col])

        for index, row in data.iterrows():
            param_dict = {k:row[k] for k in cols}
            db.insert_movie(**param_dict)

        print(db.query_all_movies())

def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_movies)
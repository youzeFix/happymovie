import sqlite3

import click
from flask import current_app, g
from flask.app import Flask
from flask.cli import with_appcontext
import pathlib
from typing import Tuple, List
import pandas
import datetime
from .utils import parse_movies_excel

def get_db():
    if 'db' not in g:
        g.db = DB()

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db._db.executescript(f.read().decode('utf8'))

class DB:

    def __init__(self) -> None:
        # auto init db
        if pathlib.Path(current_app.config['DATABASE']).exists() is False and current_app.config['AUTO_INIT_DB']:
            current_app.logger.info('auto init db')
            self._db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            self._db.row_factory = sqlite3.Row
            with current_app.open_resource('schema.sql') as f:
                self._db.executescript(f.read().decode('utf8'))
        else:
            self._db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            self._db.row_factory = sqlite3.Row

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
        with self._db:
            self._db.execute(INSERT_MOVIE_STATEMENT, sql_params)

    def insert_movie_by_userid(self, movie_name:str, movie_runtime:int, movie_rating:float, creator_id:int, movie_likability:int=1, 
                                have_seen:int=0, origin:str=None, create_time:datetime.datetime=None):
        loc = locals()
        del loc['self']
        sql_column = list(loc.keys())
        if create_time is None:
            sql_column.remove('create_time')
        
        INSERT_MOVIE_STATEMENT = f'''
        INSERT INTO movies ({','.join(sql_column)}) VALUES ({','.join(['?']*len(sql_column))}) 
        '''

        sql_params = ([loc[key] for key in sql_column])
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(INSERT_MOVIE_STATEMENT, sql_params)
            return cursor.lastrowid

    def insert_movie_df_by_userid(self, movie_df:pandas.DataFrame, creator_id:int):
        for _, row in movie_df.iterrows():
            param_dict = {k:row[k] for k in movie_df.columns}
            self.insert_movie_by_userid(**param_dict, creator_id=creator_id)
            

    def query_all_movies(self) -> List[Tuple]:
        QUERY_ALL_MOVIE_STATEMENT = '''
        SELECT * FROM movies
        '''
        res = []
        for row in self._db.execute(QUERY_ALL_MOVIE_STATEMENT):
            res.append(tuple(row))

        return res

    def query_all_movies_by_userid(self, user_id:int) -> List:
        STATEMENT = '''
        SELECT * FROM movies WHERE creator_id=?
        '''
        res = []
        for row in self._db.execute(STATEMENT, (user_id,)):
            res.append(row)

        return res

    def query_all_movies_havent_seen(self) -> List[Tuple]:
        STATEMENT = '''
        SELECT * FROM movies WHERE have_seen=0
        '''
        res = []
        for row in self._db.execute(STATEMENT):
            res.append(tuple(row))
        return res

    def query_all_movies_havent_seen_by_userid(self, user_id:int) -> List[Tuple]:
        STATEMENT = '''
        SELECT * FROM movies WHERE have_seen=0 AND creator_id=?
        '''
        res = []
        for row in self._db.execute(STATEMENT, (user_id,)):
            res.append(row)
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

    def query_last_insert_row_by_userid(self, user_id:int) -> Tuple:
        all_movies = self.query_all_movies_by_userid(user_id)
        return all_movies[-1]

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

    def query_user_by_username(self, username:str) -> Tuple:
        STATEMENT = '''
        SELECT * FROM user WHERE username = ?
        '''
        res = self._db.execute(STATEMENT, (username,)).fetchone()
        return res

    def query_all_users(self) -> List[Tuple]:
        STATEMENT = '''
        SELECT * FROM user
        '''
        res = []
        for row in self._db.execute(STATEMENT):
            res.append(tuple(row))
        return res

    def query_user_by_id(self, id:int) -> Tuple:
        STATEMENT = '''
        SELECT * FROM user WHERE id = ?
        '''
        res = self._db.execute(STATEMENT, (id,)).fetchone()
        return res

    def insert_user(self, username:str, password:str, nickname:str='DearJohn'):
        STATEMENT = '''
        INSERT INTO user (username, password, nickname) VALUES (?, ?, ?)
        '''
        with self._db:
            cursor = self._db.cursor()
            cursor.execute(STATEMENT, (username, password, nickname))
            return cursor.lastrowid

        
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    # Clear the existing data and create new tables.
    init_db()
    click.echo('Initialized the databases.')

@click.command('import-movies')
@click.option('--filename', default='movies.xlsx', help='xlsx file name to be imported')
@click.option('--creatorid', 'creator_id', help='creator id')
@with_appcontext
def import_movies(filename, creator_id):
    with current_app.open_resource(filename) as f:
        data = parse_movies_excel(f)

        db = get_db()
        # 插入数据库
        db.insert_movie_df_by_userid(data, creator_id)

        print(db.query_all_movies())

def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_movies)
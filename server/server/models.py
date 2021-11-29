from flask_sqlalchemy import SQLAlchemy
import datetime
from typing import NamedTuple
from datetime import date
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

user_movie_table = db.Table(
    'user_movie',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('likability', db.Integer, default=1),
    db.Column('have_seen', db.Boolean, default=False),
    db.Column('comment', db.String(500)),
    db.Column('create_time', db.DateTime, default=datetime.datetime.now())
)

class User(db.Model):
    field_list = ['id', 'nickname', 'username']
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), default='DearJohn')
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # 0:普通用户 1:管理员
    usertype = db.Column(db.Integer, nullable=False, default=0)
    movies = db.relationship('Movie', secondary=user_movie_table, lazy='subquery', 
                                backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User id=%d, nickname=%r, username=%r>' % (self.id, self.nickname, self.username)

movie_starring_table = db.Table(
    'movie_starring',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('starring_id', db.Integer, db.ForeignKey('starring.id'), primary_key=True)    
)

movie_genre_table = db.Table(
    'movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Starring(db.Model):
    field_list = ['id', 'name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Genre(db.Model):
    field_list = ['id', 'genre']
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(10), unique=True, nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    # 导演
    director = db.Column(db.PickleType)
    # 编剧
    scriptwriter = db.Column(db.PickleType)
    starring = db.relationship('Starring', secondary=movie_starring_table, lazy='subquery', 
                                backref=db.backref('movies', lazy=True))
    genre = db.relationship('Genre', secondary=movie_genre_table, lazy='subquery',
                                backref=db.backref('movies', lazy=True))
    # 地区
    region = db.Column(db.String(100))
    # 语言
    language = db.Column(db.PickleType)
    # 上映日期
    release_date = db.Column(db.PickleType)
    # 片长
    runtime = db.Column(db.PickleType, nullable=False)
    # 又名
    alternate_name = db.Column(db.PickleType)
    # 评分
    rating = db.Column(db.Float, nullable=False)
    # imdb
    imdb = db.Column(db.String(50))

class ReleaseDate(NamedTuple):
    '''
    上映时间
    '''
    # 地区
    region: str
    # 上映时间
    release_date: date

class RunningTime(NamedTuple):
    '''
    片长
    '''
    # 版本
    version: str
    # 时长（分钟数）
    running_time: int
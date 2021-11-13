from flask_sqlalchemy import SQLAlchemy
import datetime
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

class User(db.Model):
    field_list = ['id', 'nickname', 'username']
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), default='DearJohn')
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # 0:普通用户 1:管理员
    usertype = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<User id=%d, nickname=%r, username=%r>' % self.id, self.nickname, self.username

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

class Movie(db.Model):
    field_list = ['id', 'name', 'starring', 'genre', 'runtime', 'rating', 'likability', 'have_seen', 'comment', 'create_time']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    starring = db.relationship('Starring', secondary=movie_starring_table, lazy='subquery', 
                                backref=db.backref('movies', lazy=True))
    genre = db.relationship('Genre', secondary=movie_genre_table, lazy='subquery',
                                backref=db.backref('movies', lazy=True))
    runtime = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    likability = db.Column(db.Integer, default=1)
    have_seen = db.Column(db.Boolean, default=False)
    comment = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('movies', lazy=True))

class Starring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(10), unique=True, nullable=False)


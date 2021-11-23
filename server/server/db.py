from .models import db, User, Movie, Starring, Genre
import pandas
import datetime
import logging

logger = logging.getLogger(__name__)

def query_user_by_username(username:str) -> User:
    res = User.query.filter_by(username=username).first()
    return res

def insert_user(username:str, password:str, nickname:str=None) -> int:
    user = ''
    if nickname != None or nickname != '':
        user = User(nickname=nickname, username=username, password=password)
    else:
        user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user.id

def query_user_by_id(id:int) -> User:
    res = User.query.get(id)
    return res

def insert_movie_df_by_userid(movie_df:pandas.DataFrame, creator_id:int):
    for _, row in movie_df.iterrows():
        param_dict = {k:row[k] for k in movie_df.columns}
        insert_movie_by_userid(**param_dict, creator_id=creator_id)

def query_starring(name:str) -> Starring:
    if name is not None:
        res = Starring.query.filter_by(name=name).first()
        return res
    return None

def query_starring_by_filter(contains:str) -> list[Starring]:
    res = []
    if contains is not None:
        res = Starring.query.filter(Starring.name.contains(contains)).all()
    return res

def query_all_starring() -> list[Starring]:
    return Starring.query.all()

def query_genre(genre:str) -> Genre:
    if genre is not None:
        res = Genre.query.filter_by(genre=genre).first()
        return res
    return None

def query_genre_by_filter(contains:str) -> list[Genre]:
    res = []
    if contains is not None:
        res = Genre.query.filter(Genre.genre.contains(contains)).all()
    return res

def query_all_genre() -> list[Genre]:
    return Genre.query.all()

def turn_starring_list(starrings:list[str]) -> list[Starring]:
    res = []
    for s in starrings:
        temp = query_starring(s)
        if temp is None:
            res.append(Starring(name=s))
        else:
            res.append(temp)
    return res

def turn_genre_list(genres:list[str]) -> list[Genre]:
    res = []
    for g in genres:
        temp = query_genre(g)
        if temp is None:
            res.append(Genre(genre=g))
        else:
            res.append(temp)
    return res

def insert_movie_by_userid(name:str, runtime:int, rating:float, creator_id:int, 
                            starring:list[str]=None, genre:list[str]=None, likability:int=1, 
                            have_seen:bool=False, comment:str=None, create_time:datetime.datetime=None) -> int:
    loc = locals()
    loc['starring'] = turn_starring_list(starring)
    loc['genre'] = turn_genre_list(genre)

    movie = Movie(**loc)

    db.session.add(movie)
    db.session.commit()
    return movie.id

def query_all_movies_by_userid(user_id:int) -> list[Movie]:
    return Movie.query.filter_by(creator_id=user_id).all()

def query_all_movies_havent_seen_by_userid(user_id:int) -> list[Movie]:
    return Movie.query.filter_by(have_seen=False, creator_id=user_id).all()

def query_movie(id) -> Movie:
    return Movie.query.get(id)

def remove_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()

def update_movie(id:int, starring:list[str]=None, genre:list[str]=None, runtime:int=None, rating:float=None, 
                    likability:int=None, have_seen:int=None, comment:str=None):
    params = locals()
    del params['id']
    sql_params = {k:v for k,v in params.items() if v is not None}

    if starring is not None:
        sql_params['starring'] = turn_starring_list(starring)
    if genre is not None:
        sql_params['genre'] = turn_genre_list(genre)

    movie = Movie.query.get(id)
    if movie is None:
        logger.error(f'movie {id} not exist')
        return
    
    for k,v in sql_params.items():
        setattr(movie, k, v)

    db.session.add(movie)
    db.session.commit()
    

from .models import db, User, Movie, Starring, Genre, ReleaseDate, RunningTime, user_movie_table
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
        insert_movie_by_userid(**param_dict, user_id=creator_id)

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

def query_user_movie_map(user_id:int, movie_id:int):
    sel = user_movie_table.select().where(user_movie_table.c.user_id==user_id, user_movie_table.c.movie_id==movie_id)
    res = db.engine.connect().execute(sel).first()
    return res

def query_user_movies_map(user_id:int):
    sel = user_movie_table.select().where(user_movie_table.c.user_id==user_id)
    res = db.engine.connect().execute(sel).all()
    return res

def insert_user_movie_map(user_id:int, movie_id:int, likability:int=1, have_seen:bool=False, comment:str=None, 
                        create_time:datetime.datetime=None):
    loc = locals()
    if create_time == None:
        del loc['create_time']
    ins = user_movie_table.insert()
    ins = ins.values(**loc)
    db.engine.connect().execute(ins)

def update_user_movie_map(user_id:int, movie_id:int, likability:int=None, have_seen:bool=None, comment:str=None, 
                        create_time:datetime.datetime=None):
    params = locals()
    del params['user_id']
    del params['movie_id']
    sql_params = {k:v for k,v in params.items() if v is not None}

    upd = user_movie_table.update()
    upd = upd.values(**sql_params)
    
    db.engine.connect().execute(upd)

def delete_user_movie_map(user_id:int, movie_id:int):
    del_ins = user_movie_table.delete()
    print(del_ins)
    print(type(del_ins))
    del_ins = del_ins.where(user_movie_table.c.user_id==user_id, user_movie_table.c.movie_id==movie_id)

    db.engine.connect().execute(del_ins)

def query_all_movies_by_userid(user_id:int) -> list[Movie]:
    user = User.query.get(user_id)
    res = user.movies
    return res

def query_all_movies_havent_seen_by_userid(user_id:int) -> list[Movie]:
    return Movie.query.filter_by(have_seen=False, creator_id=user_id).all()

def query_movie(id) -> Movie:
    return Movie.query.get(id)

def query_movie_with_userinfo(user_id:int, movie_id:int) -> dict:
    '''
    return dict: {id, name, starring, genre, rating, runtime, likability, have_seen, comment, create_time}
    '''
    from .utils import get_default_runtime
    user_movie_map = query_user_movie_map(user_id, movie_id)
    movie_info = query_movie(movie_id)
    res = {}
    res['id'] = movie_info.id
    res['name'] = movie_info.name
    res['starring'] = [s.name for s in movie_info.starring]
    res['genre'] = [g.genre for g in movie_info.genre]
    res['runtime'] = get_default_runtime(movie_info.runtime).running_time
    
    res['likability'] = user_movie_map.likability
    res['have_seen'] = user_movie_map.have_seen
    res['comment'] = user_movie_map.comment
    res['create_time'] = user_movie_map.create_time
    return res


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
    
def insert_movie(name:str, runtime:list[RunningTime], rating:float, director:list[str]=None, scriptwriter:list[str]=None, 
                starring:list[str]=None, genre:list[str]=None, region:str=None, language:list[str]=None, 
                release_date:list[ReleaseDate]=None,  alternate_name:list[str]=None, imdb:str=None) -> int:
    loc = locals()
    loc['starring'] = turn_starring_list(starring)
    loc['genre'] = turn_genre_list(genre)

    movie = Movie(**loc)

    db.session.add(movie)
    db.session.commit()
    return movie.id

def query_movie_by_name(name:str) -> Movie:
    res = Movie.query.filter_by(name=name).first()
    return res

def query_movie_match_name(name:str) -> list[Movie]:
    '''
    名称匹配电影，目前直接用包含，后续改用模糊匹配
    '''
    return query_movie_contains_name(name)

def query_movie_contains_name(name:str) -> list[Movie]:
    res = []
    if name is not None:
        res = Movie.query.filter(Movie.name.contains(name)).all()
    return res

def query_all_movies() -> list[Movie]:
    res = Movie.query.all()
    return res
from flask import Blueprint, g, request, current_app
import json
import logging
from ..utils import datetime_to_json, get_time_string, get_default_runtime, match_movie
import datetime
from ..pick_algo import pick_movies_by_num, pick_movies_by_time
from .auth import login_required
import pandas
import pathlib
from ..crawler import get_page_text, parse_detail_page

from .. import db

logger = logging.getLogger(__name__)
bp = Blueprint('movies', __name__, url_prefix='/movie')

@bp.route('/all', methods=['GET'])
@login_required
def get_all_movies():
    user_id = g.user.id
    # user_id = 1
    user_movies_map = db.query_user_movies_map(user_id)
    res = []
    keys = ['likability', 'have_seen', 'comment', 'create_time']
    movie_keys = ['id', 'name', 'rating']
    if user_movies_map:
        for row in user_movies_map:
            temp = {k:getattr(row, k) for k in keys}
            movie = db.query_movie(row.movie_id)
            for key in movie_keys:
                temp[key] = getattr(movie, key)
            temp['runtime'] = get_default_runtime(movie.runtime).running_time
            temp['starring'] = [s.name for s in movie.starring]
            temp['genre'] = [g.genre for g in movie.genre]
            res.append(temp)
        
    data = {'statusCode':0, 'message':'query success', 'data':res}

    return json.dumps(data, default=datetime_to_json, ensure_ascii=False)


@bp.route('/', methods=['POST'])
@login_required
def insert_one_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}

    req_params = {key:r.get(key) for key, _ in r.items()}
    if req_params.get('create_time') is not None:
        try:
            req_params['create_time'] = datetime.datetime.strptime(req_params.get('create_time'), '%Y-%m-%d %H:%M:%S')
            print(req_params['create_time'])
        except Exception as e:
            print(e)
            return {'statusCode': -1, 'message':'date format must match %Y-%m-%d %H:%M:%S'}

    user_id = g.user.id
    # user_id = 1
    # 先去库中匹配电影，若匹配不到则创建一个，movie_id为匹配到的或新创建的movie
    temp_l = db.query_movie_match_name(req_params['name'])
    matcher = match_movie(temp_l, {'rating':req_params['rating'], 'runtime':req_params['runtime']})
    movie_id = -1
    if matcher == None:
        movie_id = db.insert_movie(req_params['name'], [db.RunningTime('default', int(req_params['runtime']))], req_params['rating'],
                                    starring=req_params['starring'], genre=req_params['genre'])
    else:
        movie_id = matcher.id

    db.insert_user_movie_map(user_id, movie_id, req_params['likability'], req_params['have_seen'], req_params['comment'], req_params['create_time']) 

    data = db.query_movie_with_userinfo(user_id, movie_id)

    res = {'statusCode': 0, 'message':'insert movie success', 'data': data}

    return json.dumps(res, default=datetime_to_json, ensure_ascii=False)


@bp.route('/', methods=['PUT'])
@login_required
def update_one_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}
    elif r.get('id') is None:
        logger.warning('update data does not contain id')
        print(r)
        return {'statusCode': -1, 'message':'update data must contain id'}
    
    r['movie_id'] = r['id']
    del r['id']

    db.update_user_movie_map(g.user.id, **r)

    return {'statusCode': 0, 'message':'update movie success'}


@bp.route('/', methods=['DELETE'])
@login_required
def remove_one_movie():
    movie_id = request.args.get('id', None)
    if id is None:
        logger.warning('id is None!')
        return {'statusCode': -1, 'message':'delete method request id param'}

    db.delete_user_movie_map(g.user.id, movie_id)

    return {'statusCode': 0, 'message':'remove movie success'}


@bp.route('/pick', methods=['POST'])
@login_required
def pick_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}

    pick_type = r.get('type')
    data = r.get('data')
    if data.get('value') == '':
        logger.error('value can not be null')
        return {'statusCode': -1, 'message':'value can not be null'}
    if pick_type is None or data is None:
        logger.error('pick_type or data is null, parameter error')
        return {'statusCode': -1, 'message':'pick_type or data is null, parameter error'}

    movies_havent_seen = db.query_all_movies_havent_seen_by_userid(g.user.id)

    starrings = data.get('starring')
    genres = data.get('genre')

    def filter_by_starring_and_genre(row):
        for s in starrings:
            if row['starring'] is None:
                return False
            temp = db.query_starring(s)
            if temp is None:
                return False
            elif temp.name not in row['starring']:
                return False

        for g in genres:
            if row['genre'] is None:
                return False
            temp = db.query_genre(g)
            if temp is None:
                return False
            elif temp.genre not in row['genre']:
                return False
        return True

    movies_input = list(filter(filter_by_starring_and_genre, movies_havent_seen))

    # type=1, pick by time; type=2, pick by num
    pick_res = []
    if pick_type == 1:
        pick_res = pick_movies_by_time(int(data.get('value')), movies_input)
    elif pick_type == 2:
        pick_res = pick_movies_by_num(int(data.get('value')), movies_input)

    res = {'statusCode': 0, 'message':'pick successful', 'data': pick_res}

    return json.dumps(res, default=datetime_to_json, ensure_ascii=False)
    
@bp.route('/export', methods=['GET'])
@login_required
def export_movies_data():
    userid = g.user.id
    movies = db.query_all_movies_with_userinfo(userid)
    export_filename = ''
    if movies:
        field_list = ['id', 'name', 'rating', 'starring', 'genre', 'runtime', 'likability', 'have_seen', 'comment', 'create_time']
        movies_input = []
        for m in movies:
            temp = {k:m.get(k) for k in field_list}
            movies_input.append(temp)
        df = pandas.DataFrame(movies_input, columns=field_list)
        columns_to_drop = ['id']
        for col in columns_to_drop:
            del df[col]
        # print(df)
        def convert_list(m):
            if m:
                return '/'.join(m)
            return
        def convert_haveseen(have_seen):
            if have_seen == True:
                return '是'
            elif have_seen == False:
                return '否'
            return ''
        df['starring'] = df['starring'].apply(convert_list)
        df['genre'] = df['genre'].apply(convert_list)
        df['have_seen'] = df['have_seen'].apply(convert_haveseen)
        time_string = get_time_string()
        export_filename = f'{userid}-export-{time_string}.xlsx'
        export_path = pathlib.Path(current_app.config['DOWNLOAD_FOLDER'])
        if export_path.exists() is False:
            export_path.mkdir()
        
        df.to_excel(export_path.joinpath(export_filename))
    else:
        return {'statusCode': 0, 'message':'there are no movies'}

    return {'statusCode': 0, 'message':'export successful', 'data': {'filename': export_filename}}

@bp.route('/starrings', methods=['GET'])
@login_required
def get_starrings():
    filter_args = request.args.get('filter')
    starrings = []
    if filter_args is None:
        starrings = db.query_all_starring()
    else:
        starrings = db.query_starring_by_filter(filter_args)
    res = []
    if starrings:
        keys = starrings[0].field_list
        for row in starrings:
            temp = {k:getattr(row, k) for k in keys}
            res.append(temp)
        
    data = {'statusCode':0, 'message':'query success', 'data':res}

    return data

@bp.route('/genres', methods=['GET'])
@login_required
def get_genres():
    filter_args = request.args.get('filter')
    genres = []
    if filter_args is None:
        genres = db.query_all_genre()
    else:
        genres = db.query_genre_by_filter(filter_args)
    
    res = []
    if genres:
        keys = genres[0].field_list
        for row in genres:
            temp = {k:getattr(row, k) for k in keys}
            res.append(temp)
        
    data = {'statusCode':0, 'message':'query success', 'data':res}

    return data

@bp.route('/movie', methods=['GET'])
@login_required
def get_match_movie():
    match_q = request.args.get('match')
    if match_q is None:
        logger.warning('match is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'parameter match is required'}

    match_res = db.query_movie_match_name(match_q)

    keys = ['id', 'name', 'starring', 'genre', 'rating', 'runtime']

    def filter_field(movie:db.Movie):
        temp = {k:getattr(movie,k) for k in keys}
        temp['starring'] = [s.name for s in movie.starring]
        temp['genre'] = [g.genre for g in movie.genre]
        temp['runtime'] = get_default_runtime(movie.runtime).running_time
        return temp

    map_res = list(map(filter_field, match_res))
    
    data = {'statusCode':0, 'message':'query success', 'data': map_res}

    return data

@bp.route('/parse_url', methods=['POST'])
@login_required
def parse_movie_by_url():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}

    url = r.get('url')
    if url is None or url == '':
        logger.error('url is null, parameter error')
        return {'statusCode': -1, 'message':'url is null, parameter error'}

    try:
        page_text = get_page_text(url)
        movie = parse_detail_page(page_text)

        # # 如果不存在则存入数据库
        # temp_l = db.query_movie_match_name(movie.movie_name)
        # if len(temp_l) == 0:
        #     db.insert_movie()

        movie_data = {'movie_name': movie.movie_name, 'starring': movie.starring[:5], 'category': movie.category, 
                        'running_time': movie.running_time[0].running_time, 'rating_num': movie.rating_num}
        
        data = {'statusCode':0, 'message':'parse success', 'data': movie_data}
        return data
    except Exception as e:
        logger.error('parse url fail')
        print(e)
        data = {'statusCode':-1, 'message':'parse error'}
        return data

    
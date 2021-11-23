from flask import Blueprint, g, request, current_app
import json
import logging
from ..utils import datetime_to_json, get_time_string
import datetime
from ..pick_algo import pick_movies_by_num, pick_movies_by_time
from .auth import login_required
import pandas
import pathlib

from .. import db

logger = logging.getLogger(__name__)
bp = Blueprint('movies', __name__, url_prefix='/movie')

@bp.route('/all', methods=['GET'])
@login_required
def get_all_movies():
    db_res = db.query_all_movies_by_userid(g.user.id)
    # print(db_res)
    res = []
    if db_res:
        keys = db_res[0].field_list
        for row in db_res:
            temp = {k:getattr(row, k) for k in keys}
            temp['starring'] = [s.name for s in temp['starring']]
            temp['genre'] = [g.genre for g in temp['genre']]
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

    temp_params = {key:r.get(key) for key, _ in r.items()}
    if temp_params.get('create_time') is not None:
        try:
            temp_params['create_time'] = datetime.datetime.strptime(temp_params.get('create_time'), '%Y-%m-%d %H:%M:%S')
            print(temp_params['create_time'])
        except Exception as e:
            print(e)
            return {'statusCode': -1, 'message':'date format must match %Y-%m-%d %H:%M:%S'}

    temp_params['creator_id'] = g.user.id
    insert_id = db.insert_movie_by_userid(**temp_params)

    row = db.query_movie(insert_id)
    data = {k:getattr(row, k) for k in row.field_list}
    data['starring'] = [s.name for s in data['starring']]
    data['genre'] = [g.genre for g in data['genre']]

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

    db.update_movie(**r)

    return {'statusCode': 0, 'message':'update movie success'}


@bp.route('/', methods=['DELETE'])
@login_required
def remove_one_movie():
    movie_id = request.args.get('id', None)
    if id is None:
        logger.warning('id is None!')
        return {'statusCode': -1, 'message':'delete method request id param'}

    db.remove_movie(movie_id)

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
            if row.starring is None:
                return False
            temp = db.query_starring(s)
            if temp is None:
                return False
            elif temp not in row.starring:
                return False

        for g in genres:
            if row.genre is None:
                return False
            temp = db.query_genre(g)
            if temp is None:
                return False
            elif temp not in row.genre:
                return False
        return True

    movies_input = list(filter(filter_by_starring_and_genre, movies_havent_seen))

    # type=1, pick by time; type=2, pick by num
    pick_res = []
    if pick_type == 1:
        pick_res = pick_movies_by_time(int(data.get('value')), movies_input)
    elif pick_type == 2:
        pick_res = pick_movies_by_num(int(data.get('value')), movies_input)

    data = []
    keys = []
    if pick_res:
        keys = pick_res[0].field_list
    for row in pick_res:
        temp = {k:getattr(row, k) for k in keys}
        temp['starring'] = [s.name for s in temp['starring']]
        temp['genre'] = [g.genre for g in temp['genre']]
        data.append(temp)

    res = {'statusCode': 0, 'message':'pick successful', 'data': data}

    return json.dumps(res, default=datetime_to_json, ensure_ascii=False)
    
@bp.route('/export', methods=['GET'])
@login_required
def export_movies_data():
    userid = g.user.id
    movies = db.query_all_movies_by_userid(userid)
    export_filename = ''
    if movies:
        field_list = movies[0].field_list
        movies_input = []
        for m in movies:
            temp = {k:getattr(m, k) for k in field_list}
            temp['starring'] = [s.name for s in temp['starring']]
            temp['genre'] = [g.genre for g in temp['genre']]
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
            if have_seen == 1:
                return '是'
            elif have_seen == 0:
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
from flask import Blueprint, g, request, current_app
import json
import logging
from ..utils import datetime_to_json
import datetime
from ..pick_algo import pick_movies_by_time
from .auth import login_required

from ..db import get_db

logger = logging.getLogger(__name__)
bp = Blueprint('movies', __name__, url_prefix='/movie')

@bp.route('/all', methods=['GET'])
@login_required
def get_all_movies():
    db = get_db()
    db_res = db.query_all_movies_by_userid(g.user['id'])
    # print(db_res)
    res = []

    for row in db_res:
        res.append({
            'index': row[0],
            'movie_name': row[1],
            'movie_runtime': row[2],
            'movie_rating': row[3],
            'movie_likability': row[4],
            'have_seen': row[5],
            'origin': row[6],
            'create_time': row[7]
        })
        
    data = {'statusCode':0, 'message':'query success', 'data':res}

    return json.dumps(data, default=datetime_to_json, ensure_ascii=False)


@bp.route('/', methods=['POST'])
@login_required
def insert_one_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}

    db = get_db()

    temp_params = {key:r.get(key) for key, _ in r.items()}
    if temp_params.get('create_time') is not None:
        try:
            temp_params['create_time'] = datetime.datetime.strptime(temp_params.get('create_time'), '%Y-%m-%d %H:%M:%S')
            print(temp_params['create_time'])
        except Exception as e:
            print(e)
            return {'statusCode': -1, 'message':'date format must match %Y-%m-%d %H:%M:%S'}

    temp_params['creator_id'] = g.user['id']
    lastrowid = db.insert_movie_by_userid(**temp_params)

    row = db.query_one_movie_by_id(lastrowid)
    data = {
        'index': row[0],
        'movie_name': row[1],
        'movie_runtime': row[2],
        'movie_rating': row[3],
        'movie_likability': row[4],
        'have_seen': row[5],
        'origin': row[6],
        'create_time': row[7]
    }

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

    db = get_db()

    db.update_movie(**r)

    return {'statusCode': 0, 'message':'update movie success'}


@bp.route('/', methods=['DELETE'])
@login_required
def remove_one_movie():
    movie_id = request.args.get('id', None)
    if id is None:
        logger.warning('id is None!')
        return {'statusCode': -1, 'message':'delete method request id param'}

    db = get_db()
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
    value = int(r.get('value'))
    if pick_type is None or value == 0:
        logger.error('pick_type or value is null, parameter error')
        return {'statusCode': -1, 'message':'pick_type or value is null, parameter error'}

    db = get_db()

    movies_havent_seen = db.query_all_movies_havent_seen_by_userid(g.user['id'])

    pick_res = pick_movies_by_time(value, movies_havent_seen)

    data = []
    for row in pick_res:
        data.append({
            'index': row[0],
            'movie_name': row[1],
            'movie_runtime': row[2],
            'movie_rating': row[3],
            'movie_likability': row[4],
            'have_seen': row[5],
            'origin': row[6],
            'create_time': row[7]
        })

    res = {'statusCode': 0, 'message':'pick successful', 'data': data}

    return json.dumps(res, default=datetime_to_json, ensure_ascii=False)
    


    
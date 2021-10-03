from flask import Blueprint, g, request, current_app
import json
import logging
from .utils import datetime_to_json
import datetime

from .db import get_db

# logger = current_app.logger
logger = logging.getLogger(__name__)
bp = Blueprint('movies', __name__, url_prefix='/movie')


@bp.route('/all', methods=['GET'])
def get_all_movies():
    db = get_db()
    db_res = db.query_all_movies()
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

    return json.dumps(res, default=datetime_to_json, ensure_ascii=False)


@bp.route('/', methods=['POST'])
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
    db.insert_movie(**temp_params)

    row = db.query_last_insert_row()
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
def remove_one_movie():
    movie_id = request.args.get('id', None)
    if id is None:
        logger.warning('id is None!')
        return {'statusCode': -1, 'message':'delete method request id param'}

    db = get_db()
    db.remove_movie(movie_id)

    return {'statusCode': 0, 'message':'remove movie success'}


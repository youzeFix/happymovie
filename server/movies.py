from flask import Blueprint, g, request, current_app
import json

from db import get_db

logger = current_app.logger
bp = Blueprint('movies', __name__, url_prefix='/movie')


@bp.route('/all', methods=('GET'))
def get_all_movies():
    db = get_db()
    res = db.query_all_movies()

    return json.dumps(res, ensure_ascii=False)


@bp.route('/', methods=('POST'))
def insert_one_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}

    db = get_db()

    temp_params = [r.get(key) for key, _ in r.items()]
    db.insert_movie(*temp_params)

    return {'statusCode': 0, 'message':'insert movie success'}


@bp.route('/', methods=('PUT'))
def update_one_movie():
    r = request.get_json()
    if r is None:
        logger.warning('req_data is none, may be content-type is not application/json!')
        return {'statusCode': -1, 'message':'req data is not json'}
    elif r.get('id') is None:
        logger.warning('update data does not contain id')
        return {'statusCode': -1, 'message':'update data must contain id'}

    db = get_db()

    db.update_movie(**r)

    return {'statusCode': 0, 'message':'update movie success'}


@bp.route('/', methods=('DELETE'))
def remove_one_movie():
    movie_id = request.args.get('id', None)
    if id is None:
        logger.warning('id is None!')
        return {'statusCode': -1, 'message':'delete method request id param'}

    db = get_db()
    db.remove_movie(movie_id)

    return {'statusCode': 0, 'message':'remove movie success'}


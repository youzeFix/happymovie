import functools

import logging
from flask import (
    Blueprint, g, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

logger = logging.getLogger(__name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.query_user_by_username(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            if nickname != '':
                db.insert_user(username, generate_password_hash(password), nickname)
            else:
                db.insert_user(username, generate_password_hash(password))
            return {'statusCode':0, 'message':'register user success'}

    return {'statusCode':-1, 'message':f'register user fail, {error}'}

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.query_user_by_username(username)
        if user:
            print(tuple(user))

        if user is None:
            error = f'Incorrect username.[{username}]'
            logger.error(error)
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            logger.error(error+password)

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            data = dict(user)
            del data['password']
            return {'statusCode':0, 'message':'login success', 'data':data}

    return {'statusCode':-1, 'message':f'login fail, {error}'}

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().query_user_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return {'statusCode':0, 'message':'login out success'}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {'statusCode':-1, 'message':'login required'}

        return view(**kwargs)

    return wrapped_view
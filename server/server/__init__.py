import os

from flask import Flask
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
        # print(app.config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from .models import db
    db.init_app(app)

    from .blueprint import movies, auth, files
    from . import db
    db.init_app(app)
    app.register_blueprint(movies.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(files.bp)
    
    return app
from celery import Celery
from .crawler import get_single_movie_info
from .db import update_movie, insert_movie
import logging

celery = Celery(__name__)
celery.config_from_envvar('CELERY_CONFIG')
logger = logging.getLogger(__name__)

def init_celery_app(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

@celery.task
def add_together(a, b):
    return a + b

@celery.task
def crawl_movie_info(movie_name:str, update_id:int=None):
    movie = get_single_movie_info(movie_name)
    if update_id is not None:
        update_movie(update_id, **{k:getattr(movie, k) for k in movie.__dataclass_fields__})
        logging.info(f'celery update movie index:{update_id} name:{movie.movie_name}')
    else:
        insert_movie(**{k:getattr(movie, k) for k in movie.__dataclass_fields__})
        logging.info(f'celery insert movie name:{movie.movie_name}')

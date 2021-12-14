from celery import Celery

celery = Celery(__name__)
celery.config_from_envvar('CELERY_CONFIG')

def init_celery_app(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

@celery.task()
def add_together(a, b):
    return a + b
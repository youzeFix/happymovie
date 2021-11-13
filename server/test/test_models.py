from threading import local
import unittest
from server import create_app
from server.models import db, User, Movie, Starring, Genre

class TestModelsMethods(unittest.TestCase):

    def test_create_all(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            db.create_all()

    def test_drop_all(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            db.drop_all()

    def test_insert_user(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            test_user = User(username='usiel1', password='123456')
            db.session.add(test_user)
            db.session.commit()
            res = User.query.all()
            print(res)

    def test_insert_starring(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            # s1 = Starring(name='actor1')
            # s2 = Starring(name='actor2')
            # db.session.add(s1)
            # db.session.add(s2)
            # db.session.commit()
            res = Starring.query.all()
            print(res)
            s = Starring.query.filter_by(name='actor1').first()
            print(s in res)

    def test_insert_genre(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            g1 = Genre(genre='genre1')
            g2 = Genre(genre='genre2')
            db.session.add(g1)
            db.session.commit(g2)
            res = User.query.all()
            print(res)

    def test_insert_movie(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            s1 = Starring.query.filter_by(name='actor1').first()
            s2 = Starring(name='actor2')
            # m1 = Movie(name='movie1', starring=[s1], genre=[Genre(genre='genre1')], runtime=11, rating=1.1, likability=1, have_seen=True,
            #             comment='comment11', creator_id=1)
            m2 = Movie(name='movie2', starring=[s1, s2], genre=[Genre(genre='genre2')], runtime=22, rating=2.2, likability=2, have_seen=True,
                        comment='comment11', creator_id=1)
            # db.session.add(m1)
            db.session.add(m2)
            db.session.commit()
            res = Movie.query.all()
            print(res)

    def test_relation(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            m2 = Movie.query.filter_by(name='movie2').first()
            print(m2)
            starrings = m2.starring
            print(starrings)
            s1 = starrings[0]
            ms = s1.movies
            print(ms)

    def test_query_movie(self):
        app = create_app()
        with app.app_context():
            db.init_app(app)
            m2 = Movie.query.filter_by(name='movie2').first()
            print('res')
            print(m2.field_list)


import unittest
from server import create_app
from server.db import get_db
import pprint

class TestDBMethods(unittest.TestCase):

    def test_query_all_movies(self):
        app = create_app()
        with app.app_context():
            db = get_db()
            res = db.query_all_movies()
            pprint.pprint(res)

    def test_query_all_movies_by_userid(self):
        app = create_app()
        with app.app_context():
            db = get_db()
            res = db.query_all_movies_by_userid(1)
            pprint.pprint(res)

    def test_query_all_user(self):
        app = create_app()
        with app.app_context():
            db = get_db()
            res = db.query_all_users()
            pprint.pprint(res)

    def test_query_user_by_username(self):
        app = create_app()
        with app.app_context():
            db = get_db()
            res = db.query_user_by_username('usiel1')
            print(dict(res))

    def test_insert_user(self):
        app = create_app()
        with app.app_context():
            db = get_db()
            res = db.insert_user('usiel3', '123456')
            print(res)
            res = db.query_all_users()
            print(res)

    # def test_update_movie(self):
    #     update_movie(1, movie_rating=9.6, have_seen=1)


if __name__ == "__main__":
    unittest.main()
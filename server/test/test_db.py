import unittest
from server import create_app
import server.db as db
import pprint

class TestDBMethods(unittest.TestCase):

    # def test_query_all_movies(self):
    #     app = create_app()
    #     with app.app_context():
    #         res = db.query_all_movies()
    #         pprint.pprint(res)

    def test_query_all_movies_by_userid(self):
        app = create_app()
        with app.app_context():
            res = db.query_all_movies_by_userid(1)
            pprint.pprint(res)

    def test_query_all_user(self):
        app = create_app()
        with app.app_context():
            res = db.query_all_users()
            pprint.pprint(res)

    def test_query_user_by_username(self):
        app = create_app()
        with app.app_context():
            res = db.query_user_by_username('usiel1')
            print(dict(res))

    def test_insert_user(self):
        app = create_app()
        with app.app_context():
            res = db.insert_user('usiel3', '123456')
            print(res)
            res = db.query_all_users()
            print(res)

    def test_insert_movie(self):
        app = create_app()
        with app.app_context():
            res = db.insert_movie_by_userid('movie1111', '100', '9.6', 1, ['周杰伦', '林俊杰'], ['genre1', 'genre2'])
            # print(res)
            res = db.query_all_movies_by_userid(1)
            for r in res:
                print(r['starring'])


if __name__ == "__main__":
    unittest.main()
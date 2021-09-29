import unittest
from server.db import get_db
import pprint

class TestDBMethods(unittest.TestCase):

    def test_query_all_movies(self):
        from flask import current_app
        with current_app.app_context():
            db = get_db()
            res = db.query_all_movies()
            pprint.pprint(res)

    # def test_insert_movie(self):
    #     insert_movie('movie111', 101, 9.8)
    #     res = get_all_movies()
    #     print(res)

    # def test_update_movie(self):
    #     update_movie(1, movie_rating=9.6, have_seen=1)


if __name__ == "__main__":
    unittest.main()
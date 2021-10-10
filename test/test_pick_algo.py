import unittest
from server.pick_algo import get_maximized_pleasure, Movie, pick_movies_by_time
from server.db import get_db
from server import create_app
from pprint import pprint

class TestPickAlgoMethods(unittest.TestCase):

    def test_get_maximized_pleasure(self):
        time_have = 400
        movies = []
        movies.append(Movie(1,142,'肖申克的救赎',-9.7))
        movies.append(Movie(2,194,'泰坦尼克号',-9.4))
        movies.append(Movie(3,148,'盗梦空间',-9.3))
        movies.append(Movie(4,103,'楚门的世界',-9.3))
        movies.append(Movie(5,116,'控方证人',-9.6))
        movies.append(Movie(6,112,'触不可及',-9.3))
        movies.append(Movie(7,132,'活着',-9.3))
        movies.append(Movie(8,118,'罗马假日',-9.0))

        res = get_maximized_pleasure(time_have, movies)
        pprint(res)

    def test_pick_movies_by_time(self):
        app = create_app()
        time_have = 400
        with app.app_context():
            db = get_db()
            movies = db.query_all_movies()
            res = pick_movies_by_time(time_have, movies)
            pprint(res)

        

if __name__ == "__main__":
    unittest.main()
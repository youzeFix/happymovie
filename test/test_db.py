import unittest
from ..db import db, get_all_movies, insert_movie, update_movie

class TestDBMethods(unittest.TestCase):

    def test_insert_movie(self):
        insert_movie('movie111', 101, 9.8)
        res = get_all_movies()
        print(res)

    def test_update_movie(self):
        update_movie(1, movie_rating=9.6, have_seen=1)


if __name__ == "__main__":
    unittest.main()
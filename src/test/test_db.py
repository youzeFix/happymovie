import unittest
from ..db import db, get_all_movies, insert_movie

class TestDBMethods(unittest.TestCase):

    def test_insert_movie(self):
        insert_movie('movie111', 101, 9.8)
        res = get_all_movies()
        print(res)


if __name__ == "__main__":
    unittest.main()
import unittest
from server.pick_algo import get_maximized_pleasure, Movie
from pprint import pprint

class TestMainMethods(unittest.TestCase):

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
        

if __name__ == "__main__":
    unittest.main()

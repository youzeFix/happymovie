import unittest
from ..main import get_maximized_pleasure, Movie, request_douban_movie, get_douban_top250
from pprint import pprint
import warnings

warnings.simplefilter('ignore', ResourceWarning)
class TestMainMethods(unittest.TestCase):

    def test_get_maximized_pleasure(self):
        time_have = 400
        movies = []
        movies.append(Movie(142,'肖申克的救赎',9.7))
        movies.append(Movie(194,'泰坦尼克号',9.4))
        movies.append(Movie(148,'盗梦空间',9.3))
        movies.append(Movie(103,'楚门的世界',9.3))
        movies.append(Movie(116,'控方证人',9.6))
        movies.append(Movie(112,'触不可及',9.3))
        movies.append(Movie(132,'活着',9.3))
        movies.append(Movie(118,'罗马假日',9.0))

        res = get_maximized_pleasure(time_have, movies)
        pprint(res)

    def test_get_douban_movie(self):
        request_douban_movie()


    def test_get_douban_top250(self):
        get_douban_top250()



if __name__ == "__main__":
    unittest.main()

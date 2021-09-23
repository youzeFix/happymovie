import unittest
from ..main import get_maximized_pleasure, Movie, request_douban_movie, get_douban_top250
from pprint import pprint
import warnings
from ..douban import get_proxy
import requests

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

    def test_proxy(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://movie.douban.com/top250",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
        }
        url = 'https://www.baidu.com'
        
        max_retries = 0
        while max_retries < 20:
            try:
                proxy = get_proxy()
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy
                }
                print(proxies)
                res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
                print(res.status_code)
                self.assertEqual(res.status_code, 200)
                if res.status_code == 200:
                    break
            except Exception as e:
                print(e)
                max_retries+=1
                print('retry', max_retries)
        

if __name__ == "__main__":
    unittest.main()

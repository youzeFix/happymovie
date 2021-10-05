import unittest
from server.crawler import get_douban_top250, get_proxy
import requests
import warnings

warnings.simplefilter('ignore', ResourceWarning)

class TestCrawlerMethods(unittest.TestCase):

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
import unittest

import pandas
from server.crawler import get_douban_top250, get_movies_brief_info, get_proxy, parse_favorite_movie, search_douban_movie_url, parse_detail_page, get_page_text, get_movies_info, parse_excel,\
                            get_movies_brief_info, parse_detail_page_runtime_and_rating
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


    def test_parse_favorite_movie(self):
        parse_favorite_movie()

    def test_search_douban_movie(self):
        detail_url = search_douban_movie_url('反贪风暴3')
        print(detail_url)

    def test_parse_detail_page(self):
        url = 'https://movie.douban.com/subject/26871906/'
        page_text = get_page_text(url)
        # with open('detail_page_demo.html', 'w', encoding='utf-8') as f:
            # f.write(page_text)
        # page_text = open('detail_page_demo.html', 'r', encoding='utf-8').read()
        movie = parse_detail_page(page_text)
        print(movie)
        df = pandas.DataFrame([movie])
        print(df)

    def test_parse_detail_page_runtime_and_rating(self):
        # url = 'https://movie.douban.com/subject/25900945/'
        # page_text = get_page_text(url)
        # with open('detail_page_demo.html', 'w', encoding='utf-8') as f:
        #     f.write(page_text)
        page_text = open('detail_page_demo.html', 'r', encoding='utf-8').read()
        movie = parse_detail_page_runtime_and_rating(page_text)
        df = pandas.DataFrame([movie])
        print(df)

    def test_get_movies_info(self):
        movie_name = ['无间道', '绿皮书', '泰坦尼克号', '倩女幽魂']
        df = get_movies_info(movie_name)
        print(df)
        df.to_excel('test_auto_movie.xlsx')

    def test_get_movies_brief_info(self):
        movie_name = ['猎狐行动','暗战2','暗战','愤怒的黄牛','华尔街之狼','负重前行','角头','觉醒','建国大业','建军大业','缉毒风暴','兴风作浪','独孤九剑']
        df = get_movies_brief_info(movie_name)
        print(df)

    def test_crawl(self):
        df = pandas.read_excel('favorite_movies.xlsx', 'Sheet2')
        movies_name = list(df['movie_name'])
        df = get_movies_brief_info(movies_name)
        df.to_excel('favorite_movie_auto_populate_brief.xlsx')

    def test_parse_excel(self):
        parse_excel()

import requests
import brotli
from lxml import etree
import pandas
import numpy as np
import random
import time
import logging
import json
import pathlib
from typing import List, Dict, NamedTuple
from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass
from datetime import date
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', 
                    level=logging.INFO, filename='douban.log', encoding='utf-8')

DEBUG = False
PROXY_ENABLE = False
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Referer": "https://movie.douban.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

def get_page_text(url):
    if DEBUG:
        with open('doubanpage.html', 'r', encoding='utf-8') as f:
            text = f.read()
            return text
    if PROXY_ENABLE:
        max_retries = 0
        while max_retries < 10:
            try:
                proxy = get_proxy()
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy
                }
                print(proxies)
                res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
                print(res.status_code)
                if res.headers.get('Content-Encoding') == 'br':
                    data = brotli.decompress(res.content)
                    text = data.decode('utf-8')
                    return text
                else:
                    return res.text
            except Exception:
                max_retries+=1
                print('retry', max_retries)

    else:
        res = requests.get(url, headers=headers, timeout=15)
        print(res.status_code)
        if res.headers.get('Content-Encoding') == 'br':
            data = brotli.decompress(res.content)
            text = data.decode('utf-8')
            return text
        else:
            return res.text

def get_proxy():
    response = requests.get("http://106.55.169.250:5010/get/").json()
    return response.get("proxy")

def get_douban_top250():
    DOUBAN_URL = 'https://movie.douban.com/top250?start={}&filter='
    movie_list = []
    try:
        for i in range(200, 250, 25):
            url = DOUBAN_URL.format(i)
            list_page_text = get_page_text(url)
            time.sleep(random.randint(5,10))
            list_page = etree.HTML(list_page_text)
            cards = list_page.xpath(r'//ol[@class="grid_view"]/li')
            for card in cards:
                title = card.xpath(r'.//div[@class="hd"]/a//text()')
                title = ','.join(title)
                title = title.replace('\n', '').replace(' ','').replace('\xa0', '').replace(',','')
                title_link = card.xpath(r'.//div[@class="hd"]/a/@href')[0].strip()
                rating = card.xpath(r'.//span[@class="rating_num"]/text()')[0].strip()
                detail_page_text = get_page_text(title_link)
                time.sleep(random.randint(5,10))
                detail_page = etree.HTML(detail_page_text)
                movie_runtime = detail_page.xpath(r'//span[@property="v:runtime"]/text()')[0]
                print('title:', title, 'rating:', rating, 'movie_runtime', movie_runtime, 'title_link', title_link)
                logging.info(f'title:{title},rating:{rating},movie_runtime:{movie_runtime},title_link:{title_link}')
                movie_list.append((title, rating, movie_runtime))
    except Exception as e:
        print(e)
        logging.error(e)


    df = pandas.DataFrame(np.array(movie_list), columns=('movie_name', 'rating', 'movie_runtime'))
    return df


def parse_favorite_movie():
    
    file_num = 0
    current_file = pathlib.Path(f'instance/favorite_movie_page{str(file_num)}.json')
    categories = []
    titles = []
    while current_file.exists():
        with open(current_file, 'r', encoding='utf-8') as f:
            obj = json.loads(f.read())
            items = obj['data']['model']['items']
            
            for i in items:
                category = i.get('category')
                title = i.get('title')
                print(f'category:{category}, title:{title}')
                categories.append(category)
                titles.append(title)
        file_num += 1
        current_file = pathlib.Path(f'instance/favorite_movie_page{str(file_num)}.json')


    df = pandas.DataFrame({'category': categories, 'title': titles})
    df.to_excel('favorite_movies.xlsx')

class ReleaseDate(NamedTuple):
    '''
    上映时间
    '''
    # 地区
    region: str
    # 上映时间
    release_date: date

class RunningTime(NamedTuple):
    '''
    片长
    '''
    # 版本
    version: str
    # 时长（分钟数）
    running_time: int


@dataclass
class Movie:
    '''
    豆瓣电影实体类
    '''
    # 电影名称
    movie_name: str
    # 导演
    director: List[str]
    # 编剧
    scriptwriter: List[str]
    # 主演
    starring: List[str]
    # 类型
    category: List[str]
    # 地区
    region: str
    # 语言
    language: List[str]
    # 上映日期
    release_date: List[ReleaseDate]
    # 片长
    running_time: List[RunningTime]
    # 又名
    alternate_name: List[str]
    # imdb
    imdb: str
    # 电影评分
    rating_num: float
    # 海报链接
    bg: str
    # 简介
    summary: str


def parse_detail_page(page_text:str) -> Movie:
    '''
    param page_text: 详情页面源码
    return : 一个包含电影详情各个字段的dict
    '''
    detail_page = etree.HTML(page_text)
    movie_name = detail_page.xpath(r'//span[@property="v:itemreviewed"]/text()')[0].strip()
    rating_num = detail_page.xpath(r'//strong[@property="v:average"]/text()')[0].strip()
    info_div = detail_page.xpath(r'//div[@id="info"]')[0]
    # print(len(info_div))
    origin = etree.tounicode(info_div)
    origin = origin.replace('\n', '')
    origin = origin.replace(' ', '')
    # print(origin)
    origin_list = origin.split('<br/>')
    parse_list = []
    for o in origin_list:
        s = etree.HTML(o)
        if s is not None:
            parse_list.append(''.join(s.xpath('//text()')))
    director = parse_list[0].split(':')[1].split('/')
    scriptwriter = parse_list[1].split(':')[1].split('/')
    starring = parse_list[2].split(':')[1].split('/')
    category = parse_list[3].split(':')[1].split('/')
    region = parse_list[4].split(':')[1].split('/')
    language = parse_list[5].split(':')[1].split('/')
    temp_release_date = parse_list[6].split(':')[1].split('/')
    release_date = []
    for e in temp_release_date:
        match_res = re.match('^(.+)\((.+)\)', e)
        if match_res is not None:
            release_date.append(ReleaseDate(match_res.group(2), match_res.group(1)))

    temp_running_time = parse_list[7].split(':')[1].split('/')
    running_time = []
    for e in temp_running_time:
        match_res = re.match('^(.+)\((.+)\)', e)
        if match_res is not None:
            run_time = match_res.group(1).split('分钟')[0]
            running_time.append(RunningTime(match_res.group(2), run_time))
        else:
            run_time = e.split('分钟')[0]
            running_time.append(RunningTime(None, run_time))
    
    alternate_name = parse_list[8].split(':')[1].split('/')
    imdb = ''
    if len(parse_list) > 9:
        imdb = parse_list[9].split(':')[1]

    movie = Movie(movie_name, director, scriptwriter, starring, category, region, language, release_date, running_time, alternate_name, imdb, rating_num)
    return movie

def parse_detail_page_runtime_and_rating(page_text:str) -> Dict:
    '''
    只解析详情页的电影市场和评分
    '''
    detail_page = etree.HTML(page_text)
    movie_name = detail_page.xpath(r'//span[@property="v:itemreviewed"]/text()')[0].strip()
    rating_num = detail_page.xpath(r'//strong[@property="v:average"]/text()')[0].strip()
    movie_runtime = detail_page.xpath(r'//span[@property="v:runtime"]/text()')[0].strip()
    temp_running_time = movie_runtime.split('/')
    running_time = []
    for e in temp_running_time:
        match_res = re.match('^(.+)\((.+)\)', e)
        if match_res is not None:
            run_time = match_res.group(1).split('分钟')[0]
            running_time.append(RunningTime(match_res.group(2), run_time))
        else:
            run_time = e.split('分钟')[0]
            running_time.append(RunningTime(None, run_time))
    if len(running_time) <= 0:
        logging.error('parse running time fail')
        return {}
    return {'movie_name': movie_name, 'running_time':running_time[0].running_time, 'rating_num':rating_num}


def search_douban_movie_url(movie_name:str) -> str:
    '''
    根据电影名称获取电影详情页的url
    '''
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://movie.douban.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    url = 'https://movie.douban.com/j/subject_suggest'
    params = {'q': movie_name}

    if PROXY_ENABLE:
        max_retries = 0
        while max_retries < 10:
            try:
                proxy = get_proxy()
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy
                }
                print(proxies)
                res = requests.get(url, params=params, headers=headers, verify=False, timeout=10)
                res = res.json()
                detail_url = None
                if len(res) > 0:
                    detail_url = res[0]['url']
                    parse_result = urlparse(detail_url)
                    detail_url = urlunparse(parse_result._replace(query=''))
                else:
                    print('search url res:', res)
                return detail_url
            except Exception:
                max_retries+=1
                print('retry', max_retries)
    else:
        res = requests.get(url, params=params, headers=headers, verify=False, timeout=10)
        res = res.json()
        # print(res)
        detail_url = None
        num = 0
        if len(res) > 0:
            while res[num]['episode'] != "":
                if num >= len(res):
                    num += 1
                    break
                num += 1
            if num > len(res):
                return detail_url
            detail_url = res[num]['url']
            parse_result = urlparse(detail_url)
            detail_url = urlunparse(parse_result._replace(query=''))
        else:
            print('search url res:', res)
        return detail_url

def get_single_movie_info(movie_name:str) -> Movie:
    detail_url = search_douban_movie_url(movie_name)
    if detail_url is None:
        print(f'movie {movie_name} get no url')
        return None
    page_text = get_page_text(detail_url)
    movie = parse_detail_page(page_text)
    return movie


def get_movies_info(movies_name:List[str]) -> pandas.DataFrame:
    '''
    根据电影名称抓取电影信息
    param movies_name: 电影名称列表
    return : 包含电影名称、导演、编剧、主演、类型、制片国家/地区、语言、上映日期、片长、又名和imdb列的dataframe
    '''
    movies = []
    total = len(movies_name)
    for index, m in enumerate(movies_name):
        time.sleep(random.randint(5,10))
        print(f'start {index+1}/{total}')
        try:
            movie = get_single_movie_info(m)
            if movie is None:
                logging.error(f'get movie {m} info failed')
                continue
            print(f'get {m} info success')
            print(movie)
            movies.append(movie)
        except Exception as e:
            print(e)
            print('exception occoured while scratch movie ' + m)

    df = pandas.DataFrame(movies)
    return df

def get_movies_brief_info(movies_name:List[str]) -> pandas.DataFrame:
    '''
    根据电影名称抓取电影简要信息
    param movies_name: 电影名称列表
    return : 包含电影名称、片长和评分的dataframe
    '''
    movies = []
    total = len(movies_name)
    fail_list = []
    for index, m in enumerate(movies_name):
        time.sleep(random.randint(5,10))
        print(f'start {index+1}/{total}')
        try:
            detail_url = search_douban_movie_url(m)
            if detail_url is None:
                print(f'movie {m} get no url')
                fail_list.append(m)
                continue
            time.sleep(random.randint(5,10))
            page_text = get_page_text(detail_url)
            movie = parse_detail_page_runtime_and_rating(page_text)
            if len(movie) > 0:
                print(f'get {m} info success')
                print(movie)
            else:
                logging.error(f'get {m} fail')
                continue
            movies.append(movie)
        except Exception as e:
            print(e)
            print('exception occoured while scratch movie ' + m)

    print('fail list:', fail_list)
    df = pandas.DataFrame(movies)
    return df

def parse_excel() -> pandas.DataFrame:
    df = pandas.read_excel('favorite_movie_auto_populate.xlsx')
    print(df['running_time'])


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/26871906/'
    page_text = get_page_text(url)
    movie = parse_detail_page(page_text)
    df = pandas.DataFrame([movie])
    print(df)
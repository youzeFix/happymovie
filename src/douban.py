import requests
import brotli
from lxml import etree
import pandas
import numpy as np
import random
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', 
                    level=logging.INFO, filename='douban.log', encoding='utf-8')

DEBUG = False
PROXY_ENABLE = False
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Referer": "https://movie.douban.com/top250",
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
        res = requests.get(url, headers=headers, timeout=5)
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
        for i in range(0, 250, 25):
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

if __name__ == "__main__":
    logging.info('start crawl')
    df = get_douban_top250()
    print(df)
    df.to_excel('top250.xlsx')

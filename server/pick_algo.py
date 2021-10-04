from heapq import nlargest, heappush, heappop
from typing import List
from dataclasses import dataclass, field
from bisect import bisect_left
import requests
from selenium import webdriver
import pandas
import numpy as np
from multiprocessing import Pool, Queue


@dataclass(order=True)
class Movie:
    movie_id: int=field(compare=False)
    movie_length: int=field(compare=False)
    movie_name: str=field(compare=False)
    movie_rating: float
    movie_likability: int=field(compare=False)

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def get_maximized_pleasure(time_have: int, movies_origin: List[Movie]) -> List[Movie]:
    def toggle_rating(x):
        x.movie_rating=-x.movie_rating
        return x
    movies = list(map(toggle_rating, movies_origin))
    n = len(movies)
    curr = 0
    movies.sort(key=lambda x:x.movie_length)
    res = []
    movies_length = [m.movie_length for m in movies]
    
    pq = []
    time_spend = 0
    while True:
        while curr < n and movies[curr].movie_length <= time_have-time_spend:
            heappush(pq, movies[curr])
            curr += 1

        if pq:
            temp_movie = heappop(pq)
            res.append(temp_movie)
            time_spend += temp_movie.movie_length
        else:
            break

        try:
            movie_index = index(movies_length, temp_movie.movie_length)
            del movies[movie_index]
        except ValueError:
            print('value error')
            break
        pq.clear()
        curr = 0
        movies_length = [m.movie_length for m in movies]
        n=len(movies)
    
    res = list(map(toggle_rating, res))
    return res



def request_douban_movie(start, end, step=25):
    DOUBAN_URL = 'https://movie.douban.com/top250?start={}&filter='
    browser = webdriver.Edge()
    movie_list = []
    for i in range(start, end, step):
        url = DOUBAN_URL.format(i)
        browser.get(url)
        cards = browser.find_elements_by_xpath(r'//ol[@class="grid_view"]/child::*')

        
        for card in cards:
            title = card.find_element_by_xpath(r'.//div[@class="hd"]/a').text.strip()
            title_link = card.find_element_by_xpath(r'.//div[@class="hd"]/a').get_attribute('href')
            rating = card.find_element_by_xpath(r'.//span[@class="rating_num"]').text.strip()
            # print('title:', title, 'rating:', rating)
            if len(browser.window_handles) == 1:
                browser.execute_script('window.open()')
            browser.switch_to.window(browser.window_handles[1])
            browser.get(title_link)
            movie_runtime = browser.find_element_by_xpath(r'//span[@property="v:runtime"]').text
            browser.switch_to.window(browser.window_handles[0])
            movie_list.append((title, rating, movie_runtime))

    df = pandas.DataFrame(np.array(movie_list), columns=('movie_name', 'rating', 'movie_runtime'))
    print(df)
    # df.to_excel('top250.xlsx')
    return df

def get_proxy():
    response = requests.get("http://106.55.169.250:5010/get/").json()
    return response.get("proxy")

def test_func1(start, end, q: Queue=None):
    l = list(range(start, end, 3))
    # q.put(l)
    return l

def get_douban_top250():
    # params = [
    #     (0,13),
    #     (15,22),
    #     (26,39)
    # ]
    # tmp = list(zip(*params))
    # print(tmp)
    # res = map(test_func1, *list(zip(*params)))
    # print(list(res))
    params = [(x,x+25) for x in range(0, 50, 25)]
    print(params)

    with Pool(5) as p:
        res = p.starmap(request_douban_movie, params)
        # res = p.map(test_func1, *list(zip(*params)))
        print(res)
        df = pandas.concat(res)
        df.to_excel('top250.xlsx')
        

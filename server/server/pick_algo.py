from heapq import nlargest, heappush, heappop
from typing import List
from dataclasses import dataclass, field
from bisect import bisect_left
from .models import Movie as Movie_db

@dataclass(order=True)
class Movie:
    movie_id: int=field(compare=False)
    movie_length: int=field(compare=False)
    movie_name: str=field(compare=False)
    movie_weight: float

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def get_maximized_pleasure(time_have: int, movies_origin: List[Movie]) -> List[Movie]:
    movies = movies_origin
    n = len(movies)
    curr = 0
    movies.sort(key=lambda x:x.movie_length)
    res = []
    
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

        movies.remove(temp_movie)
        pq.clear()
        curr = 0
        n=len(movies)
    
    return res


def pick_movies_by_time(time_have:int, movies:list[Movie_db]) -> list[Movie_db]:
    movies_input = []
    movies_map = {}
    for m in movies:
        # index, movie_runtime, movie_name, movie_rating*movie_likability
        movies_input.append(Movie(m.id, m.runtime, m.name, -m.rating*m.likability))
        movies_map[m.id] = m
    pick_output = get_maximized_pleasure(time_have, movies_input)
    res = []
    for m in pick_output:
        res.append(movies_map[m.movie_id])

    return res

def get_maximized_nums(num: int, movies_origin: List[Movie]) -> List[Movie]:
    movies = movies_origin
    movies.sort(key=lambda x:x.movie_weight)
    
    return movies[:num]

def pick_movies_by_num(num:int, movies:List[Movie_db]) -> List[Movie_db]:
    movies_input = []
    movies_map = {}
    for m in movies:
        # index, movie_runtime, movie_name, movie_rating*movie_likability
        movies_input.append(Movie(m.id, m.runtime, m.name, -m.rating*m.likability))
        movies_map[m.id] = m
    pick_output = get_maximized_nums(num, movies_input)
    res = []
    for m in pick_output:
        res.append(movies_map[m.movie_id])

    return res
from heapq import nlargest, heappush, heappop
from typing import List, Tuple
from dataclasses import dataclass, field
from bisect import bisect_left

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
    
    return res


def pick_movies_by_time(time_have:int, movies:List[Tuple]) -> List[Tuple]:
    movies_input = []
    movies_map = {}
    for m in movies:
        # index, movie_runtime, movie_name, movie_rating*movie_likability
        movies_input.append(Movie(m[0], m[2], m[1], -m[3]*m[4]))
        movies_map[m[0]] = m
    pick_output = get_maximized_pleasure(time_have, movies_input)

    res = []
    for m in pick_output:
        res.append(movies_map[m.movie_id])

    return res
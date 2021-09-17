from heapq import nlargest, heappush, heappop
from typing import List
from dataclasses import dataclass, field


@dataclass(order=True)
class Movie:
    movie_length: int=field(compare=False)
    movie_name: str=field(compare=False)
    movie_rating: float


def get_maximized_pleasure(time_have: int, movies: List[Movie]) -> List[Movie]:

    n = len(movies)
    curr = 0
    movies.sort(key=lambda x:x.movie_rating, reverse=True)
    res = []
    
    pq = []
    time_spend = 0
    while True:
        while curr < n and movies[curr].movie_length <= time_have-time_spend:
            heappush(pq, -movies[curr])
            curr += 1

        if pq:
            temp_movie = heappop(pq)
            res.append(temp_movie)
            time_spend += temp_movie.movie_length
        else:
            break
    
    return res
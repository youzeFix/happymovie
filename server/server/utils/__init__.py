import datetime
import logging
import pandas
import time
from .. import db

logger = logging.getLogger(__name__)

def get_default_runtime(runtimes:list[db.RunningTime]) -> db.RunningTime:
    return runtimes[0]

def match_movie(q:list[db.Movie], row:dict) -> db.Movie:
    for m in q:
        if m.rating != row['rating']:
            continue
        for r in m.runtime:
            if r.running_time == row['runtime']:
                return m
    return None

def get_time_string():
    """
    获得形如20161010120000这样的年月日时分秒字符串
    :return:
    """
    current = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", current)

def datetime_to_json(obj:datetime):
    return obj.strftime('%Y-%m-%d %H:%M:%S')
    # return int(obj.timestamp())

def parse_movies_excel(f) -> pandas.DataFrame:
    # 必须列
    required_col = ['name', 'runtime', 'rating']
    # 列范围（所有列）
    col_scope = ['name', 'starring', 'genre', 'runtime', 'rating', 'likability', 'have_seen', 'comment']
    excel = pandas.read_excel(f)
    # 获取在列范围内的列
    cols = [col for col in excel.columns if col in col_scope]
    # 检查是否包含必须列
    for col in required_col:
        if col not in cols:
            logger.error(f'there must be {col} column')
            return

    # 提取数据
    data = excel.loc[:, cols]

    data = data.fillna('')
    # print(data)
    def transform_starring(starring: str):
        if starring:
            return starring.split('/')
        return starring

    def transform_genre(genre: str):
        if genre:
            return genre.split('/')
        return genre

    def transform_haveseen(have_seen: str):
        if have_seen == "是":
            return True
        elif have_seen == '否':
            return False
        return 0

    data['starring'] = data['starring'].apply(transform_starring)
    data['genre'] = data['genre'].apply(transform_genre)
    data['have_seen'] = data['have_seen'].apply(transform_haveseen)

    return data




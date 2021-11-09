import datetime
import logging
import pandas
import time

logger = logging.getLogger(__name__)

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
    required_col = ['movie_name', 'movie_runtime', 'movie_rating']
    # 列范围（所有列）
    col_scope = ['movie_name', 'starring', 'genre', 'movie_runtime', 'movie_rating', 'movie_likability', 'have_seen', 'origin']
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
    # 清洗数据
    def transform_runtime(movie_runtime: str):
        if not movie_runtime.isdigit():
            movie_runtime = movie_runtime.split('分钟')[0]
            if movie_runtime.isdigit():
                return movie_runtime
        else:
            return movie_runtime

        return 0
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
            return 1
        elif have_seen == '否':
            return 0
        return 0

    data['starring'] = data['starring'].apply(transform_starring)
    data['genre'] = data['genre'].apply(transform_genre)
    data['have_seen'] = data['have_seen'].apply(transform_haveseen)

    # data['movie_runtime'] = data['movie_runtime'].apply(transform_runtime)
    return data




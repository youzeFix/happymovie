import datetime
import logging
import pandas

logger = logging.getLogger(__name__)

def datetime_to_json(obj:datetime):
    return obj.strftime('%Y-%m-%d %H:%M:%S')
    # return int(obj.timestamp())

def parse_movies_excel(f) -> pandas.DataFrame:
    # 必须列
    required_col = ['movie_name', 'movie_runtime', 'movie_rating']
    # 列范围（所有列）
    col_scope = ['movie_name', 'movie_runtime', 'movie_rating', 'movie_likability', 'have_seen', 'origin']
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

    data['movie_runtime'] = data['movie_runtime'].apply(transform_runtime)
    return data




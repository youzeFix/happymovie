FROM tiangolo/uwsgi-nginx-flask:python3.9
ADD . /app
WORKDIR /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ENV HAPPYMOVIE_SETTINGS=config/production_config.py
# ENV FLASK_APP=server
# RUN ["flask", "init-db"]
FROM tiangolo/uwsgi-nginx-flask:python3.9
ADD . /app
WORKDIR /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# ENV FLASK_APP=server
# RUN ["flask", "init-db"]
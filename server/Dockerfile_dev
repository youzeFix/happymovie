FROM python:3.9.6
ADD server /server
ADD requirements.txt /
WORKDIR /
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ENV FLASK_APP=server
# ENV FLASK_ENV="development"
RUN ["flask", "init-db"]
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
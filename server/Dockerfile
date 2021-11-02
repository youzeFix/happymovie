FROM python:3.9.6
ADD . /code
WORKDIR /code
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
ENV FLASK_APP=server
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
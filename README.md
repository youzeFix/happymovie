# happymovie
happy movie, useful

## 执行测试
在根目录下执行命令
```sh
python -m test.test_pick_algo
```
测试db
```sh
python -m test.test_db
```
测试查询所有用户
```sh
python -m unittest test.test_db.TestDBMethods.test_query_all_user
```

测试单个方法
```
python -m unittest test.test_pick_algo.TestPickAlgoMethods.test_get_maximized_pleasure
```

## 启动flask
```powershell
$env:FLASK_APP = "server"
$env:FLASK_ENV = "development"
$env:HAPPYMOVIE_SETTINGS = 'config/development_config.py'
$env:CELERY_CONFIG = 'server.config.celery_dev_config'
flask run
```

### 初始化数据库
```sh
flask init-db
```

### 导入数据
```sh
flask import-movies --filename top250.xlsx --creatorid 1
```

## Docker

### 构建server镜像

```sh
docker build . -t happymovie-server
```

### 启动server镜像

```sh
docker run -d --name happymovie-server --network happymovie-net --network-alias happymovie-server -p 5000:5000 happymovie-server
```

### 构建web镜像

```sh
docker build . -t happymovie-web
```

### 启动web镜像

```sh
docker run -d --name happymovie-web --network happymovie-net --network-alias happymovie-web -p 8080:80 happymovie-web
```

### 连接到mysql数据库

```sh
docker run -it --network happymovie-net --rm mysql mysql -hhappymovie-db -uroot -p
```

## Docker-compose

### 启动

```sh
docker-compose -d up
```

### 停止

```
docker-compose down
```

## celery

启动worker

```powershell
$env:CELERY_CONFIG = 'server.config.celery_dev_config'
celery -A server.tasks worker -l info
```


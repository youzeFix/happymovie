# happymovie
happy movie, useful

## 执行测试
在根目录下执行命令
```sh
python -m test.test_main
```
测试db
```sh
python -m test.test_db
```

测试单个方法
```
python -m unittest test.test_main.TestMainMethods.test_get_maximized_pleasure
```

## 启动flask
```powershell
$env:FLASK_APP = "server"
$env:FLASK_ENV = "development"
flask run
```

### 初始化数据库
```sh
flask init-db
```

### 导入数据
```sh
flask import-movies --filename top250.xlsx
```
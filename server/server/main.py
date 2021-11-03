# 该文件是为uwsgi而创建，也可作为调试使用
from . import create_app
app = create_app()


if __name__ == "__main__":
    app.run()
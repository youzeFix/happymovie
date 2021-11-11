MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DOWNLOAD_FOLDER = 'asset'
ALLOWED_EXTENSIONS = {'xlsx'}
AUTO_INIT_DB = True

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'happymovie'
USERNAME = 'root'
PASSWORD = '123456'

DB_URI = "mysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
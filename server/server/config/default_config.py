MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DOWNLOAD_FOLDER = 'asset'
ALLOWED_EXTENSIONS = {'xlsx'}

HOST = 'happymovie-db'
PORT = '3306'
DATABASE = 'happymovie'
USERNAME = 'root'
PASSWORD = 'happymovie1234'

DB_URI = "mysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
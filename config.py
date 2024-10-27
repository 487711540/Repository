DATABASE = 'flasktest'
USERNAME = 'root'
PASSWORD = '000000'
HOST = 'localhost'
PORT = '3306'

URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = URI

import os
import yaml
DEBUG = True
APP_NAME = "beerapp"


SQLALCHEMY_ECHO = True  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

conn_type = "mysql+pymysql"  
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
port = os.environ.get('MYSQL_PORT')
DATABASE_NAME = 'msia423' 
host = os.environ.get('MYSQL_HOST')
localorRDS = os.environ.get('localorRDS')
if localorRDS == 'local':
    host = "8000"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/beers.db' 
elif localorRDS == 'RDS':
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
    format(conn_type, user, password, host, port, DATABASE_NAME)

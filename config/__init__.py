import pymysql
from decouple import config

if config('DATABASE_ENGINE') == 'mariadb':
    pymysql.install_as_MySQLdb()
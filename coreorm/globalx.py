# -*- coding: utf-8 -*-
from coreorm.db.lock.mysql import getdb

CORE_MODEL_NAME = 'CoreModel'

INNER_INSERT_FIELDS = ''
INNER_UPDATE_FIELDS = ''

MYSQL_HOST = '192.168.36.3'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '111111'
MYSQL_CONNECTION_TIMEOUT = 24*60*60

GLOBAL_DB_CONN = getdb()
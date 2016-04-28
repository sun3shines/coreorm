# -*- coding: utf-8 -*-

import time
import MySQLdb
from coreorm.globalx import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,\
    MYSQL_PASSWD,MYSQL_CONNECTION_TIMEOUT
    
class dbConn(object):

    def __init__(self,host,user,passwd,port,db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.flag = False
        self._connect_time = None
        
    def connect(self):
        
        if not self.flag:
            self.connection = MySQLdb.connect(host=self.host,user=self.user,
                                              passwd=self.passwd,port=self.port,db=self.db) 
            self.flag = True
            self._connect_time = time.time()
            
    def close(self):

        if self.flag:
            self.connection.close()
            self.flag = False

    @property
    def timeout(self):
        return time.time() > self._connect_time + MYSQL_CONNECTION_TIMEOUT
    
    def getDataList(self,sqlStr):
        sqlStr = sqlStr.encode('utf-8')

        self.connect()
        cur = self.connection.cursor()
        cur.execute(sqlStr)
        data = cur.fetchall()
        cur.close()
        self.connection.commit()
        return data
         
    def execute_sql(self,sqlStr):

        sqlStr = sqlStr.encode('utf-8')

        print sqlStr
        self.connect()
        cur = self.connection.cursor()
        cur.execute(sqlStr)
        cur.close()
        self.connection.commit()

def getDb():
    return dbConn(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT,'cloudweb')

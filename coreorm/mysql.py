# -*- coding: utf-8 -*-

import time
import MySQLdb
from globalx import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_CONNECTION_TIMEOUT
    
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
    
    def getData(self,sqlStr):
        sqlStr = sqlStr.encode('utf-8')

        self.connect()
        cur = self.connection.cursor()

        cur.execute(sqlStr)
        data = cur.fetchone()
        cur.close()
        self.connection.commit()
        return data

    def getDataList(self,sqlStr):
        sqlStr = sqlStr.encode('utf-8')

        self.connect()
        cur = self.connection.cursor()
        cur.execute(sqlStr)
        data = cur.fetchall()
        cur.close()
        self.connection.commit()
        return data

    def genAttrsStr(self,attrs):
        
        return ' , '.join(attrs)
    
    def genConditionStr(self,cdict):

        cs = ["%s = '%s'" % (str(key),str(cdict[key])) for key in cdict]
        return ' and '.join(cs)
    
    def genValsStr(self,vals):
        
        vs = ["'%s'" % (v) for v in vals]
        return ' , '.join(vs)
    
    def select(self,attrs,table,c={},e = ''):

        attrsStr = self.genAttrsStr(attrs)
        
        sqlStr = 'select %s from %s' % (attrsStr,table)
        if c:
            conditionStr = self.genConditionStr(c)
            sqlStr = sqlStr + ' where %s' % (conditionStr)  
        if e:
            sqlStr = sqlStr + e
            
        return self.getDataList(sqlStr)
         
    def execute_sql(self,sqlStr):

        sqlStr = sqlStr.encode('utf-8')

        print sqlStr
        self.connect()
        cur = self.connection.cursor()
        cur.execute(sqlStr)
        cur.close()
        self.connection.commit()

    def genUpdateValStr(self,s):
        
        ss = ["%s = '%s'" % (str(key),str(s[key])) for key in s]
        return ' , '.join(ss)
    
    def update(self,s,t,c):

        sStr = self.genUpdateValStr(s)
        sqlStr = 'update %s set %s ' % (t,sStr)
        if c:
            cStr = self.genConditionStr(c)
            sqlStr = sqlStr + ' where %s' % (cStr)
        
        self.execute_sql(sqlStr)
        return True,''
    
    def insert(self,attrs,vals,table):
        
        attrsStr = self.genAttrsStr(attrs)
        valsStr = self.genValsStr(vals)
        sqlStr = 'insert into %s (%s) values (%s)' % (table,attrsStr,valsStr)
        self.execute_sql(sqlStr) 
        return True,''
   
    def delete(self,table,condition):
        
        sqlStr = 'delete from %s' % (table)
        if condition:
            conditionStr = self.genConditionStr(condition)
            sqlStr = sqlStr + ' where %s' % (conditionStr)
        self.execute_sql(sqlStr)
                
        return True,''
     
    def splitPath(self,absPath):

        return absPath.split('/')[-1],'/'.join(absPath.split('/')[:-1])

def getDb():

    return dbConn(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT,'cloudweb')

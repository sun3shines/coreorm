
import threading

from cloudweb.db.table.mysql import dbConn
from cloudweb.platform.globalx.static import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD

class db(dbConn):
    def __init__(self,*args, **kwargs):
        
        super(db,self).__init__(*args, **kwargs)
        self.dblock = threading.Lock()
        
    def lock(self):
        return self.dblock.acquire()
    
    def unlock(self):
        self.dblock.release()

class LOCK:
    def __init__(self,conn):
        self.conn = conn

    def __enter__(self):
        self.conn.lock()
        return self

    def __exit__(self,type,value,trace):
        self.conn.unlock()

def getlock(conn):

    return LOCK(conn)
      
def getdb():

    return db(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_PORT,'cloudweb')


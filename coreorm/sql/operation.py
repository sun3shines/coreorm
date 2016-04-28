# -*- coding: utf-8 -*-

from coreorm.sql.sql import genAttrsStr,genConditionStr,genUpdateValStr,genValsStr
from coreorm.globalx import GLOBAL_DB_CONN

def db_update(kv,table,condition_kv):

    sStr = genUpdateValStr(kv)
    sqlStr = 'update %s set %s ' % (table,sStr)
    if condition_kv:
        cStr = genConditionStr(condition_kv)
        sqlStr = sqlStr + ' where %s' % (cStr)
    
    GLOBAL_DB_CONN.execute_sql(sqlStr)
    return True,''

def db_insert(attrs,vals,table):
    
    attrsStr = genAttrsStr(attrs)
    valsStr = genValsStr(vals)
    sqlStr = 'insert into %s (%s) values (%s)' % (table,attrsStr,valsStr)
    GLOBAL_DB_CONN.execute_sql(sqlStr) 
    return True,''

def db_delete(table,condition_kv):
    
    sqlStr = 'delete from %s' % (table)
    if condition_kv:
        conditionStr = genConditionStr(condition_kv)
        sqlStr = sqlStr + ' where %s' % (conditionStr)
    GLOBAL_DB_CONN.execute_sql(sqlStr)
            
    return True,''

def db_select(attrs,table,condition_kv={},extra =''):

    attrsStr = genAttrsStr(attrs)
    
    sqlStr = 'select %s from %s' % (attrsStr,table)
    if condition_kv:
        conditionStr = genConditionStr(condition_kv)
        sqlStr = sqlStr + ' where %s' % (conditionStr)  
    if extra:
        sqlStr = sqlStr + extra
        
    return GLOBAL_DB_CONN.getDataList(sqlStr)

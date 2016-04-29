# -*- coding: utf-8 -*-

from coreorm.core.fields import ForeignType
from coreorm.sql.operation import db_update,db_insert,db_delete, db_select

def instance_save(obj):
    
    table = obj.__tablename__
    if obj.modify:
        condition_kv = {'id':obj.id}
        kv = {}
        for k in obj.__d_updatefields__:
            
            if obj.__relatedfields__.has_key(k):
                kv.update({k:obj.__dict__[k]})
            else:
                kv.update({k:getattr(obj,k)})
                
        return db_update(kv, table, condition_kv)
    else:
        attrs = obj.__d_insertfields__
        vals = []
        for attr in attrs:
            if obj.__relatedfields__.has_key(attr):
                vals.append(obj.__dict__[attr])
            else:
                vals.append(getattr(obj, attr))
                
        return db_insert(attrs, vals, table)
    
def instance_delete(obj):
    
    table = obj.__tablename__
    condition_kv = {'id':obj.id}
    return db_delete(table, condition_kv)
    
def objects_get(cls,condition_kv):
    for k in condition_kv:
        if k not in cls.__m_tablefields__:
            raise KeyError
        
    table = cls.__tablename__
    attrs = cls.__d_tablefields__
    datas = db_select(attrs, table, condition_kv)
    
    if not datas:
        raise ValueError
    
    return db2obj(cls,datas[0])
    
def objects_filter(cls,condition_kv):
    
    for k in condition_kv:
        if k not in cls.__m_tablefields__:
            raise KeyError
        
    table = cls.__tablename__
    attrs = cls.__d_tablefields__
    datas = db_select(attrs, table, condition_kv)
    
    objlist = []
    for data in datas:
        obj = db2obj(cls,datas[0])
        objlist.append(obj)
        
    return objlist

def objects_values(cls):
        
    table = cls.__tablename__
    attrs = cls.__d_tablefields__
    datas = db_select(attrs, table)
    
    objlist = []
    for data in datas:
        obj = db2dict(cls,datas[0])
        objlist.append(obj)
        
    return objlist

def objects_exclude():
    # no
    pass

def objects_all(cls):

        
    table = cls.__tablename__
    attrs = cls.__d_tablefields__
    datas = db_select(attrs, table)
    
    objlist = []
    for data in datas:
        obj = db2obj(cls,data)
        objlist.append(obj)
    return objlist

def objects_orderby():
    # yes
    pass

def db2obj(cls,data):
    obj = cls()
    if len(cls.__d_tablefields__) != len(data):
        raise RuntimeError
    
    for i,attr in enumerate(cls.__d_tablefields__):
        obj.__dict__[attr]= data[i]
    return obj

def db2dict(cls,data):
    obj = {}
    if len(cls.__d_tablefields__) != len(data):
        raise RuntimeError
    
    for i,attr in enumerate(cls.__d_tablefields__):
        obj[attr]= data[i]
    return obj

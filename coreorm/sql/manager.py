# -*- coding: utf-8 -*-

from coreorm.sql.operation import db_update,db_insert,db_delete, db_select

def instance_save(obj):
    
    table = obj.__tablename__
    if obj.modify:
        condition_kv = {'id':obj.id}
        kv = {}
        for k in obj.__updatefields__:
            kv.update({k:getattr(obj,k)})
        return db_update(kv, table, condition_kv)
    else:
        attrs = obj.__insertfields__
        vals = [getattr(obj,attr) for attr in obj.__insertfields__]
        return db_insert(attrs, vals, table)
    
def instance_delete(obj):
    
    table = obj.__tablename__
    condition_kv = {'id':obj.id}
    return db_delete(table, condition_kv)
    
def objects_get(cls,condition_kv):
    for k in condition_kv:
        if k not in cls.__tablefields__:
            raise KeyError
        
    table = cls.__tablename__
    attrs = cls.__tablefields__
    datas = db_select(attrs, table, condition_kv)
    
    if not datas:
        raise ValueError
    
    return db2obj(cls,datas[0])
    
def objects_filter():
    # yes
    pass

def objects_values():
    # yes
    pass

def objects_exclude():
    # no
    pass

def objects_all():
    # yes
    pass

def objects_orderby():
    pass

def db2obj(cls,data):
    obj = cls()
    if len(cls.__tablefields__) != len(data):
        raise RuntimeError
    
    for i,attr in enumerate(cls.__tablefields__):
        setattr(obj, attr, data[i])
    return obj

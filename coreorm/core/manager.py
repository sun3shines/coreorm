# -*- coding: utf-8 -*-

from coreorm.sql.manager import objects_all,objects_exclude,objects_filter,\
    objects_get,objects_orderby,objects_values
    
class Manager(object):
    def __init__(self):
        self.cls =None
        pass

    def __get__(self,instance,cls):
        # 禁止实例化对象访问 实例了。是的。
        if instance:
            raise AttributeError
        self.cls = cls
        print 'Manager __get__' 
        # return instance.__dict__.get(self.name,None)
        return self
            
    def __set__(self,instance,value):
        raise NotImplementedError

    def get(self,*args,**kwargs):
        print 'Manager get'
        return objects_get(self.cls,kwargs)
    
    def filter(self,*args,**kwargs):
        print 'Manager filter'
        return objects_filter(self.cls,kwargs)
    
    def values(self,*args,**kwargs):
        print 'Manager values'
        return objects_values(self.cls)
    
    def all(self,*args,**kwargs):
        print 'Manager all'
        return objects_all(self.cls)
    
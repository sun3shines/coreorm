# -*- coding: utf-8 -*-

class Manager(object):
    def __init__(self):
        pass

    def __get__(self,instance,cls):
        # 禁止实例化对象访问 实例了。是的。
        if instance:
            raise AttributeError

        print 'Manager __get__' 
        # return instance.__dict__.get(self.name,None)
        return self
    
    def get(self,*args,**kwargs):
        print 'Manager get'    
        
    def __set__(self,instance,value):
        raise NotImplementedError

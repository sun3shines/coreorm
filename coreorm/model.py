# -*- coding: utf-8 -*-

from coreorm.fields import FieldType,ForeignType,StringType,IntType
from coreorm.manager import Manager
from coreorm.globalx import CORE_MODEL_NAME
from coreorm.sql.manager import instance_save,instance_delete

class ModelMeta(type):
    
    def __new__(cls,name,bases,attrs):
        
        if CORE_MODEL_NAME == name:
            return type.__new__(cls,name,bases,attrs)
        tablefields = []
        tablename = name.lower()
        primarykey = ''
        for key,val in attrs.items():
            if not isinstance(val,FieldType):
                continue
            
            if isinstance(val, ForeignType):
                val.name = key
                val.fkid_label = '_'.join([key,'id'])
            else:
                val.name = key
                if val.primary:
                    primarykey = val.name
                    
            tablefields.append(key)
            
        if 'id' not in tablefields:
            attrs['id'] = IntType('id')
            tablefields.append('id')
        if not primarykey:
            primarykey = 'id'
            
        attrs['__tablefields__'] = tablefields
        attrs['__tablename__'] = tablename
        attrs['__primarykey__'] = primarykey
        attrs['__insertfields__'] = []
        attrs['__updatefields__'] = []
        classobj = super(ModelMeta,cls).__new__(cls,name,bases,attrs)
        setattr(classobj, 'objects', Manager())
        
        return classobj
    
class CoreModel(object):
    __metaclass__ = ModelMeta    
    def __init__(self,*args,**kwargs):
        for key,val in kwargs.items():
            if key not in self.__tablefields__:
                raise TypeError('%s field not exists'% (key))
            setattr(self,key,val)

    def __setattr__(self, name,value):
        if name in self.__tablefields__: 
            if not self.update_instance:
                if name not in self.__insertfields__:
                    self.__insertfields__.append(name)
            else:
                if name not in self.__updatefields__:
                    self.__updatefields__.append(name)
        return object.__setattr__(self, name,value)
    
    @property
    def modify(self):
        return self.id
    
    def save(self):
        return instance_save(self)
    
    def delete(self):
        return instance_delete(self)
    

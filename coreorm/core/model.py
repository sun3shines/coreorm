# -*- coding: utf-8 -*-

from coreorm.core.fields import FieldType,ForeignType,StringType,IntType
from coreorm.core.manager import Manager
from coreorm.globalx.static import CORE_MODEL_NAME
from coreorm.sql.manager import instance_save,instance_delete
from coreorm.utils.ordereddict import OrderedDict

class ModelMeta(type):
    
    def __new__(cls,name,bases,attrs):
        
        if CORE_MODEL_NAME == name:
            return type.__new__(cls,name,bases,attrs)
        
        d = dict(attrs)
        
        tablefields = []
        tablename = name.lower()
        primarykey = ''
        mappings = {}
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
            mappings.update({key:val})
            
        if 'id' not in tablefields:
            idval = IntType(name='id',notnull=True,auto_increment=True)
            d['id'] = idval
            tablefields.insert(0,'id')
            mappings.update({'id':idval})
            
        if not primarykey:
            primarykey = 'id'
        # 通过obj.attr 或者getattr(obj,attr) 的方式只能获取到值，而不是对象
        # 后续的内容要求我们获取到对象了。 
        d['__mappings__'] = mappings    
        d['__tablefields__'] = tablefields
        d['__tablename__'] = tablename
        d['__primarykey__'] = primarykey
        d['__insertfields__'] = []
        d['__updatefields__'] = []
        
        classobj = super(ModelMeta,cls).__new__(cls,name,bases,d)
        setattr(classobj, 'objects', Manager())
        
        return classobj
    
    @classmethod
    def __prepare__(cls,clsname,bases):
        return OrderedDict()
    
class CoreModel(object):
    __metaclass__ = ModelMeta    
    def __init__(self,*args,**kwargs):
        for key,val in kwargs.items():
            if key not in self.__tablefields__:
                raise TypeError('%s field not exists'% (key))
            setattr(self,key,val)

    def __setattr__(self, name,value):
        if name in self.__tablefields__: 
            if not self.modify:
                if name not in self.__insertfields__:
                    self.__insertfields__.append(name)
            else:
                if name not in self.__updatefields__:
                    self.__updatefields__.append(name)
        return object.__setattr__(self, name,value)
    
    @classmethod
    def as_sql(cls):
        fields_str = ','.join([cls.__mappings__.get(f).as_sql for f in cls.__tablefields__])
        return 'CREATE table %s (%s);' % (cls.__tablename__,fields_str)
        
    @property
    def modify(self):
        return self.id
    
    def save(self):
        return instance_save(self)
    
    def delete(self):
        return instance_delete(self)
    

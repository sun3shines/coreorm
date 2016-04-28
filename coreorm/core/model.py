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
        
        m_tablefields = []
        d_tablefields = []
        
        tablename = name.lower()
        primarykey = ''
        mappings = {}
        relatedfields = {} # 为了反向查找，无法确定city_id 是否为普通id，还是foreignkey
        for key,val in attrs.items():
            if not isinstance(val,FieldType):
                continue
            
            if isinstance(val, ForeignType):
                val.name = key
                val.fkid_label = '_'.join([key,'id'])
                relatedfields.update({val.fkid_label:val.name})
                m_tablefields.append(val.name)
                d_tablefields.append(val.fkid_label)
                
            else:
                val.name = key
                if val.primary:
                    primarykey = val.name
                m_tablefields.append(key)
                d_tablefields.append(key)
                
            mappings.update({key:val})
            
        idval = attrs.get('id')
        if 'id' not in m_tablefields:
            idval = IntType(name='id',notnull=True,auto_increment=True)
            d['id'] = idval
            m_tablefields.insert(0,'id')
            d_tablefields.insert(0,'id')
            mappings.update({'id':idval})
            
        if not primarykey:
            primarykey = 'id'
            idval.primary = True
        # 通过obj.attr 或者getattr(obj,attr) 的方式只能获取到值，而不是对象
        # 后续的内容要求我们获取到对象了。 
        d['__mappings__'] = mappings    
        d['__m_tablefields__'] = m_tablefields
        d['__d_tablefields__'] = d_tablefields
        d['__tablename__'] = tablename
        d['__primarykey__'] = primarykey
        d['__d_insertfields__'] = []
        d['__d_updatefields__'] = []
        d['__relatedfields__'] = relatedfields
        
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
            if key not in self.__m_tablefields__:
                raise TypeError('%s field not exists'% (key))
            setattr(self,key,val)

    def __setattr__(self, name,value):
        
        v = self.__mappings__.get(name)
        newname = name
        
        if newname in self.__m_tablefields__:
            
            if isinstance(v, ForeignType):
                newname = v.fkid_label 
            if not self.modify:
                if newname not in self.__d_insertfields__:
                    self.__d_insertfields__.append(newname)
            else:
                if newname not in self.__d_updatefields__:
                    self.__d_updatefields__.append(newname)
        return object.__setattr__(self, name,value)
    
    @classmethod
    def as_sql(cls):
        fields_str = ','.join([cls.__mappings__.get(f).as_sql for f in cls.__m_tablefields__])
        return 'CREATE table %s (%s);' % (cls.__tablename__,fields_str)
        
    @property
    def modify(self):
        return self.id
    
    def save(self):
        return instance_save(self)
    
    def delete(self):
        return instance_delete(self)
    

# -*- coding: utf-8 -*-

from coreorm.globalx.static import FIELD_TYPE_INT,FIELD_TYPE_STRING,FIELD_TYPE_TIME

class FieldType(object):
    def __init__(self,name=None,primary=False,notnull=False,auto_increment=False):
        
        self.name = name
        self.primary=primary
        self.TypeStr = 'Field'
        
        self.notnull = notnull
        self.auto_increment = auto_increment
        
    def __get__(self,instance,cls):
        print '%s __get__' % (self.TypeStr)    
        return instance.__dict__.get(self.name,None)
        
    def __set__(self,instance,value):
        print '%s __set__ val: %s' % (self.TypeStr,str(value))
        instance.__dict__[self.name] = value

    @property
    def basetype(self):
        raise NotImplementedError

    @property
    def as_sql(self):
        return '%s %s%s%s%s' % (self.name,self.basetype,
                         ' NOT NULL' if self.notnull else '',
                         ' PRIMARY KEY' if self.primary else '',
                         ' AUTO_INCREMENT' if self.auto_increment else '')
class IntType(FieldType):
    
    def __init__(self,*args,**kwargs):
        super(IntType,self).__init__(*args,**kwargs)
        self.TypeStr = 'IntType'

    @property
    def basetype(self):
        return FIELD_TYPE_INT
        
class StringType(FieldType):
    def __init__(self,*args,**kwargs):
        super(StringType,self).__init__(*args,**kwargs)
        self.TypeStr = 'StringType'

    @property
    def basetype(self):
        return FIELD_TYPE_STRING
            
class ForeignType(FieldType):
    def __init__(self,fkcls,name=None,primary=False,notnull=False):
        
        self.fkcls = fkcls
        self.name = name
        self.fkid_label = '_'.join([name,'id']) if name else None
        
        self.primary = primary
        self.notnull = notnull
        
    def __get__(self,instance,cls):
        print 'ForeignType __get__'    
        fkid = instance.__dict__.get(self.fkid_label,None)
        return self.fkcls.objects.get(id=fkid)
        
    def __set__(self,instance,value):
        print 'ForeignType __set__'
        # self.fkid = value.id
        fkid = value.id
        instance.__dict__[self.fkid_label] = fkid 
        
    @property
    def as_sql(self):
        return '%s %s%s%s' % (self.fkid_label,self.basetype,
                         ' NOT NULL' if self.notnull else '',
                         ' PRIMARY KEY' if self.primary else '')
    @property
    def basetype(self):
        return FIELD_TYPE_INT
    
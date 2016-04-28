# -*- coding: utf-8 -*-

class FieldType(object):
    def __init__(self,name=None,primary=False):
        
        self.name = name
        self.primary=primary
        self.TypeStr = 'Field'
        
    def __get__(self,instance,cls):
        print '%s __get__' % (self.TypeStr)    
        return instance.__dict__.get(self.name,None)
        
    def __set__(self,instance,value):
        print '%s __set__ val: %s' % (self.TypeStr,str(value))

        instance.__dict__[self.name] = value

class IntType(FieldType):
    
    def __init__(self,*args,**kwargs):
        super(IntType,self).__init__(*args,**kwargs)
        self.TypeStr = 'IntType'
        
class StringType(FieldType):
    def __init__(self,*args,**kwargs):
        super(StringType,self).__init__(*args,**kwargs)
        self.TypeStr = 'StringType'
        
class ForeignType(FieldType):
    def __init__(self,fkcls,name=None):
        
        self.fkcls = fkcls
        self.name = name
        self.fkid_label = '_'.join([name,'id']) if name else None
        
    def __get__(self,instance,cls):
        print 'ForeignType __get__'    
        fkid = instance.__dict__.get(self.fkid_label,None)
        return self.fkcls.objects.get(id=fkid)
        
    def __set__(self,instance,value):
        print 'ForeignType __set__'
        # self.fkid = value.id
        fkid = value.id
        instance.__dict__[self.fkid_label] = fkid 
        
        

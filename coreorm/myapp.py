# -*- coding: utf-8 -*-

from coreorm.core.model import CoreModel
from coreorm.core.fields import StringType,ForeignType,IntType
from coreorm.core.manager import Manager

class Country(CoreModel):
    id = IntType(primary=True,notnull=True,auto_increment=True)
    name = StringType()
    
class City(CoreModel):
    name = StringType()
    country = ForeignType(Country)
    
class Person(CoreModel):
    name = StringType()
    city = ForeignType(City)
    
def test():

#    pp = Person(name='she')
#    pp = Person()
#    pp.name = 'she'
#    print pp.name
    print Country.as_sql() 
    cc = Country(name='china')
    cc.save()
    cobj = Country.objects.get(name='china')
    print cobj.id
    cobj.name = 'USA'
    cobj.save()
#    cobj.delete()
#    cobj = Country.objects.get(name='china')
#    print cobj.id
#    ci = City(name='handan',country=cc)
    # ci.country = cc
    
#    pp = Person()
#    pp.name='she'
#    pp.city = ci
    
#    print pp.city.country.name
    
    # pp.objects.get(id=1)
#    Person.objects.get(id=1)
    import pdb;pdb.set_trace()
    print Country.as_sql()
    pass
#    cc.name = 'china'
#    print cc.name 

if __name__ == '__main__':
    test()

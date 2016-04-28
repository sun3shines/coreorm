# -*- coding: utf-8 -*-

from coreorm.model import CoreModel
from coreorm.fields import StringType,ForeignType,IntType
from coreorm.manager import Manager

class Country(CoreModel):
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
      
    cc = Country(name='china')
    cc.name = 'abc'
#    ci = City(name='handan',country=cc)
    # ci.country = cc
    
#    pp = Person()
#    pp.name='she'
#    pp.city = ci
    
#    print pp.city.country.name
    
    # pp.objects.get(id=1)
#    Person.objects.get(id=1)
    import pdb;pdb.set_trace()
    pass
#    cc.name = 'china'
#    print cc.name 

if __name__ == '__main__':
    test()

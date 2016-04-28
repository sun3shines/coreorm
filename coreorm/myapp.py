# -*- coding: utf-8 -*-

from coreorm.core.model import CoreModel
from coreorm.core.fields import StringType,ForeignType,IntType

class Country(CoreModel):
    id = IntType(primary=True,notnull=True,auto_increment=True)
    name = StringType()
    
class City(CoreModel):
    name = StringType()
    country = ForeignType(Country)
    
class Person(CoreModel):
    name = StringType()
    city = ForeignType(City)
    

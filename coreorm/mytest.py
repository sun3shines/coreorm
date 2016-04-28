# -*- coding: utf-8 -*-

from coreorm.myapp import Country,City,Person

def obj_create():
    cc = Country(name='china')
    cc.save()
    cobj = Country.objects.get(name='china')
    print cobj.id
    
def obj_update():
    cobj = Country.objects.get(name='china')
    print cobj.id
    cobj.name = 'USA'
    cobj.save()

def obj_delete():
    cobj = Country.objects.get(name='USA')
    print cobj.id
    cobj.delete()

def obj_get():
    cobj = Country.objects.get(name='CN')
    print cobj.id

def foreignkey_save():

    countryobj = Country.objects.get(name='CN')
    ci = City(name='HD',country=countryobj)
    ci.save()

    
def foreignkey_get():
    cityobj = City.objects.get(name='HD')
    print cityobj.country.id
    
def foreignkey_update():
    countryobj = Country.objects.get(name='USA')
    cityobj = City.objects.get(name='HD')
    cityobj.country = countryobj
    cityobj.save()
    
def sql():
    print Country.as_sql()
    print City.as_sql()
    print Person.as_sql()

if __name__ == '__main__':
    import pdb;pdb.set_trace()
#    sql()
#    obj_create()
#    obj_update()
#    obj_delete()
#    obj_get()
#    foreignkey_save()
#    foreignkey_get()
    foreignkey_update()
    

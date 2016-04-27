# -*- coding: utf-8 -*-

class C(object):  
    a = 'abc'  
    def __getattribute__(self, *args, **kwargs):  
        print("__getattribute__() is called")  
        return object.__getattribute__(self, *args, **kwargs)  
#        return "haha"  
    def __getattr__(self, name):  
        print("__getattr__() is called ")  
        return name + " from getattr"  
      
    def __get__(self, instance, owner):  
        print("__get__() is called", instance, owner)  
        return self  
      
    def foo(self, x):  
        print(x)  
  
class C2(object):  
    d = C()  
if __name__ == '__main__':  
    c = C()  
    c2 = C2()  
##    c.a
#    print(c.a) 
 
#    print(c.zzzzzzzz)   # 访问两个函数了，先访问__getattribute__，再访问__getattr__，不是直接访问__getattr__的
#    c2.d # 不访问__getattribute__ 
    print(c2.d.a) 

# -*- coding: utf-8 -*-

def genAttrsStr(attrs):
    return ' , '.join(attrs)

def genConditionStr(cdict):

    cs = ["%s = '%s'" % (str(key),str(cdict[key])) for key in cdict]
    return ' and '.join(cs)

def genValsStr(vals):
    
    vs = ["'%s'" % (v) for v in vals]
    return ' , '.join(vs)

def genUpdateValStr(s):

    ss = ["%s = '%s'" % (str(key),str(s[key])) for key in s]
    return ' , '.join(ss)


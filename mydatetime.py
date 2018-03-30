#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
时间格式处理
"""
import time

def mydatetime(sec=None):
    t = time.localtime(sec) if sec else time.localtime()
    y = str(t.tm_year)
    m = str(t.tm_mon)
    d = str(t.tm_mday)
    h = str(t.tm_hour)
    M = str(t.tm_min)
    s = str(t.tm_sec)

    m = m if len(m) > 1 else '0' + m
    d = d if len(d) > 1 else '0' + d
    h = h if len(h) > 1 else '0' + h
    M = M if len(M) > 1 else '0' + M
    s = s if len(s) > 1 else '0' + s

    return {'year':y,'mon':m,'day':d,'hour':h,'min':M,'sec':s}

#!/usr/bin/env python
# -- coding: utf-8 --
"""
把一个SLB-1开放的端口克隆到另一个SLB-2,
SLB-2原开放端口将全部删除
使用方法: python  SLB-1  SLB-2
"""
import sys,os
from getslbinfo import GetSlbInfo
from checkargs import checkargv

try:
    slbip1 = sys.argv[1]
    slbip2 = sys.argv[2]
except:
    print('Usage: python %s sIP dIP' % sys.argv[0])
else:
    #生成要开放的端口列表
    rel1 = GetSlbInfo(slbip1)
    rel1.run()
    ports1 = rel1.listenerPorts
    ports1 = [str(x) for x in ports1]
    ports1 = ','.join(ports1)

    #生成SLB-2要被删除的端口列表
    rel2 = GetSlbInfo(slbip2)
    rel2.run()
    ports2 = rel2.listenerPorts
    ports2 = [str(x) for x in ports2]
    ports2 = ','.join(ports2)

    #删除SLB-2原有端口
    if sys.platform[:3] == 'lin':
        pipe = os.popen('/usr/local/python27/bin/python slbdeleteport.py' + ' ' + slbip2 + ' ' + ports2)
        print(pipe.read())
        pipe.close()
    else:
        pipe = os.popen('python slbdeleteport.py' + ' ' + slbip2 + ' ' + ports2)
        print(pipe.read())
        pipe.close()

    #开放SLB-2与SLB-1相同的端口
    if sys.platform[:3] == 'lin':
        pipe = os.popen('/usr/local/python27/bin/python slbaddtcpport.py' + ' ' + slbip2 + ' ' + ports1)
        print(pipe.read())
        pipe.close()
    else:
        pipe = os.popen('python slbaddtcpport.py' + ' ' + slbip2 + ' ' + ports1)
        print(pipe.read())
        pipe.close()

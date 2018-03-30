#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
设置SLB端口,先删除原有端口,再设置参数提供的端口
使用: python  slbsettcpport.py  SLB_IP Port | Port,Port,Port... | StartPort EndPort'
"""
import sys,os
from getslbinfo import GetSlbInfo
from getslbipall import GetSlbIpAll
from checkargs import checkargv

slbip = sys.argv[1]

rel = GetSlbIpAll()
rel.run()
if slbip not in rel.iplist:  #检查SLB-IP的正确
    print('IP:  %s is not exists' % slbip)
    os._exit(17)

rel = GetSlbInfo(slbip)
rel.run()
ports1 = rel.listenerPorts   #原有端口,将被删除

ports2 = checkargv()       #新开端口
if not ports2:
    print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
    os._exit(17)

ports2 = ','.join(ports2)

if ports1:
    ports1 = [str(x) for x in ports1]
    ports1 = ','.join(ports1)
    
    #删除原有端口
    if sys.platform[:3] == 'lin':
        pipe = os.popen('/usr/local/python27/bin/python slbdeleteport.py' + ' ' + slbip + ' ' + ports1)
        print(pipe.read())
        pipe.close()
    else:
        pipe = os.popen('python slbdeleteport.py' + ' ' + slbip + ' ' + ports1)
        print(pipe.read())
        pipe.close()

#开放新端口
if sys.platform[:3] == 'lin':
    pipe = os.popen('/usr/local/python27/bin/python slbaddtcpport.py' + ' ' + slbip + ' ' + ports2)
    print(pipe.read())
    pipe.close()
else:
    pipe = os.popen('python slbaddtcpport.py' + ' ' + slbip + ' ' + ports2)
    print(pipe.read())
    pipe.close()


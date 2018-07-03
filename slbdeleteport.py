#!/usr/bin/env python
# -- coding: utf-8 --
"""
删除SLB开放端口,如果端口没开放则跳过
使用方法: python slbdeleteport.py  SLB_IP Port | Port,Port,Port... | StartPort EndPort'
"""
from aliyunsdk import Aliyunsdk
from aliyunsdkslb.request.v20140515.DeleteLoadBalancerListenerRequest import DeleteLoadBalancerListenerRequest
from getslbinfo import GetSlbInfo
from getslbipall import GetSlbIpAll
from publicclass import SkipPort
import os,time

resultFormat = 'json'

class SlbDeletePort(Aliyunsdk):
    """
     把要删除的SLB  IP和端口作为参数,生成该类的实例
     一个实例只删除一个端口,多个端口需要多个实例
    """
    def __init__(self,slbIp,listenPort,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.listenPort = int(listenPort)
        self.resultFormat = resultFormat
        self.slbIp = slbIp
        self.slballip = GetSlbIpAll()
        self.slballip.run()
        if not self.slbIp in self.slballip.iplist:      #检查SLB IP是否正确,否则退出
            print('SLB IP: %s not exists' % self.slbIp)
            os._exit(17)
            
        self.slbinfo = GetSlbInfo(slbIp)
        self.slbinfo.run()
        if self.listenPort not in self.slbinfo.listenerPorts:    #检查要删除的端口是否存在,否则跳过
            raise SkipPort(self.listenPort)
        
        self.request = DeleteLoadBalancerListenerRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_LoadBalancerId(self.slbinfo.slbid)
        self.request.set_ListenerPort(self.listenPort)

    def handling(self):
        if u'RequestId' in self.result.keys():
            print('Port %s deleted' % self.listenPort)
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys
    from checkargs import checkargv

    ports = checkargv()
    if not ports:
        print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
        os._exit(17)

    slbip = sys.argv[1]
   
    for port in ports:
        time.sleep(2)
        try:
            rel = SlbDeletePort(slbip,int(port))
            rel.run()
        except SkipPort as e:
            print("Port %s is skipped" % e.port)

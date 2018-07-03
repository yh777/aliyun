#!/usr/bin/env python
# -- coding: utf-8 --
"""
添加SLB端口(在保留原有端口的基础上添加,如果端口已经存在则跳过
使用方法: python slbaddtcpport.py  SLB_IP Port | Port,Port,Port... | StartPort EndPort
"""
from aliyunsdk import Aliyunsdk
from aliyunsdkslb.request.v20140515.CreateLoadBalancerTCPListenerRequest import CreateLoadBalancerTCPListenerRequest
from getslbinfo import GetSlbInfo
from slbstartport import SlbStartPort
from getslbipall import GetSlbIpAll
from publicclass import SkipPort
import os,time

resultFormat = 'json'

class SlbAddTcpPort(Aliyunsdk):
    """
     把要开放的SLB  IP和端口作为参数,生成该类的实例
     一个实例只开放一个端口,多个端口需要多个实例
     开放一个端口的同时也会设置相同的后端端口并激活端口
    """
    def __init__(self,slbIp,listenPort,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.listenPort = int(listenPort)    #要开放的端口
        self.resultFormat = resultFormat
        self.slbIp = slbIp    #要开放端口的SLB IP
        self.slballip = GetSlbIpAll()
        self.slballip.run()
        if not self.slbIp in self.slballip.iplist:    #检查SLB IP是否有错
            print('SLB IP: %s not exists' % self.slbIp)
            os._exit(17)
            
        self.slbinfo = GetSlbInfo(slbIp)  #获取SLB的相关信息
        self.slbinfo.run()
        
        if len(self.slbinfo.listenerPorts) == 50:    #开放端口达到50个,停止添加
            print('50  Ports')
            os._exit(17)
        if self.listenPort in self.slbinfo.listenerPorts:    #如果端口已经开放则跳过
            raise SkipPort(self.listenPort)
        
        #设置相关参数
        self.request = CreateLoadBalancerTCPListenerRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_LoadBalancerId(self.slbinfo.slbid)
        self.request.set_ListenerPort(self.listenPort)
        self.request.set_BackendServerPort(self.listenPort)    #后端服务器开放的端口
        self.request.set_Bandwidth(-1)    #设置带宽,-1为不限制

    def run(self):    #重载run方法
        Aliyunsdk.run(self)    #调用父类的run依法
        sp = SlbStartPort(self.slbinfo.slbid,self.listenPort)    #激活端口
        sp.run()

    def handling(self):
        if u'RequestId' in self.result.keys():
            print('Port %s opened' % self.listenPort)
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys
    from checkargs import checkargv  #检查端口

    ports = checkargv()    #端口检查并返回端口列表
    if not ports:   #端口错误
        print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
        os._exit(17)

    slbip = sys.argv[1]
   
    for port in ports:
        time.sleep(2)
        try:
            rel = SlbAddTcpPort(slbip,int(port))
            rel.run()
        except SkipPort as e:
            print("Port %s is skipped" % e.port)

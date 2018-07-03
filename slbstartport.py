#!/usr/bin/env python
# -- coding: utf-8 --
"""
激活开放的SLB端口,一般由其它模块调用,不直接使用
"""
from aliyunsdk import Aliyunsdk
from aliyunsdkslb.request.v20140515.StartLoadBalancerListenerRequest import StartLoadBalancerListenerRequest

resultFormat = 'json'

class SlbStartPort(Aliyunsdk):
    """
    为构造函数提供SLB IP和端口
    调用run方法激活该端口
    """
    def __init__(self,slbid,port,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        self.request = StartLoadBalancerListenerRequest()
        self.request.set_LoadBalancerId(slbid)
        self.request.set_ListenerPort(port)

    def handling(self):
        pass

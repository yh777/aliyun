#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
为SLB添加后端服务器
使用:  python slbsetbackendserver  SlbIP EcsIP
"""
from aliyunsdkslb.request.v20140515.AddBackendServersRequest import AddBackendServersRequest
from aliyunsdk import Aliyunsdk
from getslbinfo import GetSlbInfo
from ecsiptoid import EcsIpToId
from slbsetname import SlbSetName    #设置完成后根据后端服务器名称重新设置SLB名称

import os

resultFormat = 'json'

class SlbSetBackendServer(Aliyunsdk):
    """
    为构造函数提供SLB IP和ECS  IP,生成一个实例
    调用run方法,设置后端服务器
    """
    def __init__(self,slbip,ecsip,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        self.slbip = slbip
        self.ecsip = ecsip

        rel = GetSlbInfo(slbip)
        rel.run()
        self.slbid = rel.slbid
        if rel.backendServerId:   #检查SLB  IP是否正确
            print('SLB: %s is used' % slbip)
            os._exit(17)

        rel = EcsIpToId(ecsip)    #通过ecs IP获得ID
        rel.run()
        self.ecsid = rel.ecsid

        self.request = AddBackendServersRequest()
        self.request.set_LoadBalancerId(self.slbid)
        self.request.set_BackendServers([{"ServerId":str(self.ecsid)}])

    def handling(self):
        if u'RequestId' in self.result.keys():
            rel = SlbSetName(self.slbip)    #重新设置SLB的名称,根据ECS的名称(服务器ID-月日)
            rel.run()
            print('ecs: %s => slb: %s is added' % (self.ecsip,self.slbip))
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys

    try:
        rel = SlbSetBackendServer(sys.argv[1],sys.argv[2])
        rel.run()
    except:
        print('Usage:  %s SlbIP EcsIP' % sys.argv[0])
    


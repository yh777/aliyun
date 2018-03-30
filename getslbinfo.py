#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
以SLB  IP为参数返回该SLB的开放端口,后端服务器IP和名称
使用方法:  python  getslbinfo  slbIP
"""
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest 
from aliyunsdk import Aliyunsdk
from slbiptoid import SlbIpToId
from ecsidtoip import EcsIdToIp

resultFormat = 'json'

class GetSlbInfo(Aliyunsdk):
    def __init__(self,address,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        self.address = address
        re = SlbIpToId(self.address)
        re.run()
        self.slbid = re.slbid
        self.request = DescribeLoadBalancerAttributeRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_LoadBalancerId(self.slbid)

    def handling(self):
        self.listenerPorts = self.result['ListenerPorts']['ListenerPort']
        self.listenerPorts.sort()
        self.slbName = self.result['LoadBalancerName']

        if self.result['BackendServers']['BackendServer']:
            self.backendServerId = str(self.result['BackendServers']['BackendServer'][0]['ServerId'])
            se = EcsIdToIp(self.backendServerId)
            se.run()
            self.backendServerIp = se.publicIp
            self.backendServerName = se.instanceName
        else:
            self.backendServerId = None
            
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys
    try:
        re = GetSlbInfo(sys.argv[1])
    except:
        print("Usage: python getslbinfo.py IPaddress")
    else:
        re.run()
        print('slbId:  %s' % re.slbid)
        print('slbIp:  %s' % re.address)
        print('slbName:  %s' % re.slbName)
        print('ListenerPorts:')
        for port in re.listenerPorts:
            print(port)
        print('BackendServerID: %s' % re.backendServerId)
        if re.backendServerId:
            print('BackendServerIP: %s' % re.backendServerIp)
            print('BackendServerName: %s' % re.backendServerName)

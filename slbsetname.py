#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
根据提供的SLB-IP和名称(如果不提供名称则根据后端服务器名称设置)设置SLB的名称,
使用:  python slbsetname.py   SlbIp [SlbName]
"""
from aliyunsdkslb.request.v20140515.SetLoadBalancerNameRequest import SetLoadBalancerNameRequest
from aliyunsdk import Aliyunsdk
from getslbipall import GetSlbIpAll
from slbiptoid import SlbIpToId
from getslbinfo import GetSlbInfo
from mydatetime import mydatetime
import os,time

resultFormat = 'json'

class SlbSetName(Aliyunsdk):
    def __init__(self,address,name=None,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        rel = GetSlbIpAll()
        rel.run()
        if address not in rel.iplist:
            print('IP:  %s is not exists' % address)
            os._exit(17)
        
        self.slbip = address
        rel = SlbIpToId(self.slbip)
        rel.run()
        self.slbid = rel.slbid
        
        #如果不提供name参数则根据服务器名称生成name
        if not name:
            rel = GetSlbInfo(self.slbip)
            rel.run()
            if rel.backendServerId:
                name = rel.backendServerName.split('-')[-1]
                t = mydatetime()
                name = name + '-' + t['year'] + t['mon'] + t['day']
            else:
                name = 'tmp'
                t = mydatetime()
                name = name + t['year'] + t['mon'] + t['day']
        self.slbname = name
        self.request = SetLoadBalancerNameRequest()
        self.request.set_LoadBalancerId(self.slbid)
        self.request.set_LoadBalancerName(self.slbname)

    def handling(self):
        if u'RequestId' in self.result.keys():
            print('Name:  %s is setted' % self.slbname)
        Aliyunsdk.handling(self)
                


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        rel = SlbSetName(sys.argv[1])
    elif len(sys.argv) == 3:
        rel = SlbSetName(sys.argv[1],sys.argv[2])
    else:
        print('Usage: python %s SlbIp [SlbName]' % sys.argv[0])
        os._exit(17)
    rel.run()
            
        

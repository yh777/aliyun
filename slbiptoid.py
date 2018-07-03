#!/usr/bin/env python
# -- coding: utf-8 --
"""
根据SLB  IP 获得SLB ID
使用方法:  python  slbiptoid.py  SLB-IP
"""
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest 
from aliyunsdk import Aliyunsdk
from getslbipall import GetSlbIpAll
import os

resultFormat = 'json'

class SlbIpToId(Aliyunsdk):
    def __init__(self,address,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        rel = GetSlbIpAll()
        rel.run()
        if address not in rel.iplist:
            print('IP:  %s is not exists' % address)
            os._exit(17)
        self.request = DescribeLoadBalancersRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_Address(address)
        self.slbid = ''

    def handling(self):
        re = self.result['LoadBalancers']['LoadBalancer'][0]
        self.slbid = re['LoadBalancerId']
        self.slbip = re['Address']
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys
    try:
        re = SlbIpToId(sys.argv[1])
    except:
        print('Usage: python SlbIpToId.py IP address')
    else:
        re.run()
        print('SlbId:    %s' % re.slbid)
        print('SlbIp:    %s' % re.slbip)
        

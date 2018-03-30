#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
提供ECS IP,返回ECS ID等信息
使用方法: python   ecsiptoid.py  EcsIP
"""
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdk import Aliyunsdk
import os

resultFormat = 'json'

class EcsIpToId(Aliyunsdk):
    """
     为构造函数提供ECS IP,
     执行run方法得到ECS 内网IP,ID,名称及区域
    """
    def __init__(self,publicIp):
        Aliyunsdk.__init__(self)
        self.publicIp = publicIp
        self.resultFormat = resultFormat
        self.request = DescribeInstancesRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_PublicIpAddresses([self.publicIp])

    def handling(self):
        try:
            self.ecsid = self.result['Instances']['Instance'][0]['InstanceId']
            self.innerIp = self.result['Instances']['Instance'][0]['InnerIpAddress']['IpAddress'][0]
            self.instanceName = self.result['Instances']['Instance'][0]['InstanceName']
            self.regionId = self.result['Instances']['Instance'][0]['RegionId']
            Aliyunsdk.handling(self)
        except IndexError:
            print('IP:  %s is not exist' % self.publicIp)
            os._exit(17)

if __name__ == '__main__':
    import sys
    try:
       re = EcsIpToId(sys.argv[1])
    except:
        print("Usage: python ecsiptoid.py PublicIP")
    else:
        re.run()
        print('PublicIp:  %s' % re.publicIp)
        print('__Ecs ID:  %s' % re.ecsid)
        print('__InstanceName:  %s' % re.instanceName)
        print('__InnerIp:  %s' % re.innerIp)
        print('__RegionId:  %s' % re.regionId)

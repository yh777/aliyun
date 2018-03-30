#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
提供ECS ID,返回ECS IP等信息
使用方法: python   ecsidtoip.py  EcsID
"""
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdk import Aliyunsdk
import os

resultFormat = 'json'

class EcsIdToIp(Aliyunsdk):
    """
     为构造函数提供ECS ID,
     执行run方法得到ECS 内网IP,外网IP,名称及区域
    """
    def __init__(self,ecsid):
        Aliyunsdk.__init__(self)
        self.ecsid = ecsid
        self.resultFormat = resultFormat
        self.request = DescribeInstancesRequest()
        self.request.set_accept_format(self.resultFormat)
        self.request.set_InstanceIds([self.ecsid])

    def handling(self):
        try:
            self.publicIp = self.result['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0]    #外网IP
            self.innerIp = self.result['Instances']['Instance'][0]['InnerIpAddress']['IpAddress'][0]       #内网IP
            self.instanceName = self.result['Instances']['Instance'][0]['InstanceName']                     #名称
            self.regionId = self.result['Instances']['Instance'][0]['RegionId']                                        #区域
            Aliyunsdk.handling(self)
        except IndexError:
            print('ID: %s is not exist' % self.ecsid)
            os._exit(17)

if __name__ == '__main__':
    import sys
    try:
       re = EcsIdToIp(sys.argv[1])
    except:
        print("Usage: python ecsidtoip.py EcsID")
    else:
        re.run()
        print('Ecs ID:  %s' % re.ecsid)
        print('__PublicIp:  %s' % re.publicIp)
        print('__InstanceName:  %s' % re.instanceName)
        print('__InnerIp:  %s' % re.innerIp)
        print('__RegionId:  %s' % re.regionId)

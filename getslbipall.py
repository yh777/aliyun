#!/usr/bin/env python
# -- coding: utf-8 --
"""
获得所有的SLB IP
使用方法: python  getslbipall.py
"""
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest 
from aliyunsdk import Aliyunsdk

resultFormat = 'json'

class GetSlbIpAll(Aliyunsdk):
    def __init__(self,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        self.request = DescribeLoadBalancersRequest()
        self.request.set_accept_format(self.resultFormat)

    def handling(self):
        self.iplist = self.result['LoadBalancers']['LoadBalancer']
        l = []
        #print('SLB IP:')
        #sum = len(self.iplist)
        for re in self.iplist:
            l.append(re['Address'])
        self.iplist = l[:]
        #for i in self.iplist:
        #    print(i)
        #print 'Total:',sum
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    try:
        re = GetSlbIpAll()
    except:
        print('Usage: python getslbinfoAll.py')
    else:
        re.run()
        print('SLB IP:')
        sum = len(re.iplist)

        for i in re.iplist:
            print(i)
        print 'Total:',sum

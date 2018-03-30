#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
根据SLB  IP删除后端服务器
使用方法:  python  slbdeletebackendserver.py  slbip
"""
from aliyunsdkslb.request.v20140515.RemoveBackendServersRequest import RemoveBackendServersRequest
from aliyunsdk import Aliyunsdk
from getslbinfo import GetSlbInfo
from slbsetname import SlbSetName    #删除后端服务器后,SLB名称被重新设置成"tmp+当前日期(月日)"

import os

resultFormat = 'json'

class SlbDeleteBackendServer(Aliyunsdk):
    """
     提供SLB  IP生成类
     调用run方法删除后端服务器
    """
    def __init__(self,slbip,resultFormat=resultFormat):
        Aliyunsdk.__init__(self)
        self.resultFormat = resultFormat
        self.slbip = slbip    #SLB  IP
        rel = GetSlbInfo(slbip)    #获得后端服务器的ID
        rel.run()
        if not rel.backendServerId:    #如果后端未设置服务器则打印信息并退出
            print("SLB: %s has not backendServer" % slbip)
            os._exit(17)
         
         #删除后端服务器
        self.slbid = rel.slbid
        self.ecsid = rel.backendServerId

        self.request = RemoveBackendServersRequest()
        self.request.set_LoadBalancerId(self.slbid)
        self.request.set_BackendServers([str(self.ecsid)])

    def handling(self):
        if u'RequestId' in self.result.keys():
            rel = SlbSetName(self.slbip)    #删除后端服务器后重新设置SLB名称
            rel.run()
            print('SLB: %s backendServer is deleted' % self.slbip)
            
        Aliyunsdk.handling(self)

if __name__ == '__main__':
    import sys
    try:
        rel = SlbDeleteBackendServer(sys.argv[1])
        rel.run()
    except:
        print('Usage: python %s slbIP' % sys.argv[0])
        

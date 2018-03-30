#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
打印所有未使用的SLB
使用:  python everyslbinfo.py(不需要任何参数)
"""
from getslbipall import GetSlbIpAll
from getslbinfo import GetSlbInfo

def geteveryslbinfo():
    """
    返回有两元素组成的元组
    第一个元素是以slb IP为键的字典(包含SLB name,后端服务器名称和IP)
    第二个元素是字符串列表,内容为每个SLB的IP,SLB名称,后端服务器IP及名称
    """
    rel = GetSlbIpAll()
    rel.run()

    slbinfod = {}
    slbips = rel.iplist

    for slbip in slbips:
        slbinfod[slbip] = {}
        slb = GetSlbInfo(slbip)
        slb.run()
        slbinfod[slbip]['slbName'] = slb.slbName
        if slb.backendServerId:
            slbinfod[slbip]['backendServerIp'] = slb.backendServerIp
            slbinfod[slbip]['backendServerName'] = slb.backendServerName
        else:
            slbinfod[slbip]['backendServerIp'] = ''
            slbinfod[slbip]['backendServerName'] = ''
    
    slbinfol = []
    for key in slbinfod:
        slbinfol.append(slbinfod[key]['slbName'] + ',' + key + ',' + slbinfod[key]['backendServerName'] + ',' + slbinfod[key]['backendServerIp'])
    slbinfol.sort()

    return (slbinfod,slbinfol)

if __name__ == '__main__':
    rel1,rel2 = geteveryslbinfo()
    for l in rel2:    #只使用的元组的第一个,打印所有后端服务器设置为空的SLB名称及IP
        if l.split(',')[2] == '':
            print(l)
        

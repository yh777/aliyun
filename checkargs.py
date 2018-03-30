#-- coding:utf-8 --
import re,sys,os

#检查SLB端口是否规范
def checkport(ports):
    for port in ports:
        if not (re.match('^[0-9]{1,}$',port) and int(port) < 65536 and int(port) > 0):
            return False
    return True

#整理端口列表
def checkargv():
    ports = []
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
        os._exit(17)
        
    if len(sys.argv) == 3:
        ports = sys.argv[2].split(',')
        ports.sort()
        if not checkport(ports):
            print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
            os._exit(17)
    elif len(sys.argv) == 4:
        i = int(sys.argv[2])
        j = int(sys.argv[3])
        while i <= j:
            ports.append(str(i))
            i += 1
        if not checkport(ports):
            print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
            os._exit(17)
    else:
        print('Usage: python %s SLB_IP Port | Port,Port,Port... | StartPort EndPort' % sys.argv[0])
        os._exit(17)
    return ports

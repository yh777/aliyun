#!/usr/local/python27/bin/python
# -- coding: utf-8 --
"""
所有类的基础类
一般不单独使用
"""
from aliyunsdkcore.client import AcsClient

#用于认证的ID,密钥,和默认区域
#accessKeyID = 'abc123'
#accessKeySecret = 'abc123'

accessKeyID = 'abc123'
accessKeySecret = 'abc123'

regionID = 'cn-hangzhou'

class Aliyunsdk(object):
    """
     __init__方法: 认证初始化并生成一个执行阿里云操作的对象(AcsClient)
     run方法: 执行阿里相关的操作并返回结果
     switch方法: 把返回的json结果转换成Python字典
     handling方法: 处理返回的结果,由其他子类重载
    """
    def __init__(self,accessKeyID=accessKeyID,
                 accessKeySecret=accessKeySecret,
                 regionID=regionID):
        self.client = AcsClient(accessKeyID,accessKeySecret,regionID)
        self.result = ''
        self.request = None

    def run(self):
        self.result = self.client.do_action_with_exception(self.request)
        if self.resultFormat == 'json':
            self.switch()
        self.handling()

    def switch(self):
        import json
        self.result = json.loads(self.result)

    def handling(self):
        pass
        #print('\n')
        #print(self.__class__.__name__)
        #print('RequestId:    %s' % self.result['RequestId'])
        

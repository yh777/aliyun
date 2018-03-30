class SkipPort(Exception):
    def __init__(self,port):
        self.port = port
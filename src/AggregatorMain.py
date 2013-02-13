# -*- coding: utf-8 -*-

import sqlite3, Pyro4
from LinkStorageProxy import LinkStorageProxy

class AggregatorMain(object):
    '''The Aggregator stores the links the crawlers find'''
    def __init__(self):
        self.linkStorageProxy = LinkStorageProxy()
        
        self.daemon = Pyro4.Daemon()
        self.nameServer = Pyro4.locateNS()
        self.uri = self.daemon.register(self.linkStorageProxy)
        self.nameServer.register("linkStorage", self.uri)
    
    def run(self):
        self.daemon.requestLoop(self._checkExit)
    
    def _checkExit(self):
        if self.linkStorageProxy.done:
            return False
        return True
        
def main():
    am = AggregatorMain()
    am.run()
            
if __name__ == '__main__':
    main()
        
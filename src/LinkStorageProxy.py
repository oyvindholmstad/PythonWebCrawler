# -*- coding: utf-8 -*-

import sys
from LinkStorage import LinkStorage
from LinkCache import LinkCache

class LinkStorageProxy(object):
    """LinkStorageProxy provides access to the LinkStorage of the Aggregator remotely through Pyro"""

    LAST_LINK = 'http://www.internetlastpage.com/'
    MAX_NUMBER_OF_LINKS_IN_CACHE = 10000
    done = False
    
    def __init__(self):
        self.linkStorage = LinkStorage()
        self.linkCache = LinkCache(LinkStorageProxy.MAX_NUMBER_OF_LINKS_IN_CACHE)
        self._fillCache()
        
    def getUnvisitedLinks(self, num):
        if LinkStorageProxy.done:
            return []

        return self.linkStorage.getUnvisitedLinks(num)
    
    def setLinkAsVisited(self, link):
        self.linkStorage.setLinkAsVisited(link)
    
    def submitNewLinks(self, links):
        l = self.linkStorage
        for link in links:
            if self.isLastLink(link):
                LinkStorageProxy.done = True
                return
            if self.linkCache.hasLink(link):
                continue
            else:
                self.linkCache.addLink(link)
                l.insertLink(link)
    
    def isLastLink(self, link):
        if link.getFullUrl() == LinkStorageProxy.LAST_LINK:
            return True
        return False
        
    def isDone(self):
        if LinkStorageProxy.done:
            return True
        else:
            return False
            
    def _fillCache(self):
        visitedLinks = self.linkStorage.getVisitedLinks(LinkStorageProxy.MAX_NUMBER_OF_LINKS_IN_CACHE)
        for link in visitedLinks:
            self.linkCache.addLink(link)
        
    def test(self):
        print 'Received test call'
        return 'OK'
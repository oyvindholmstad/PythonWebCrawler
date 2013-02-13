# -*- coding: utf-8 -*-

class LinkCache(object):
    '''LinkCache is a simple memory cache for links'''
    def __init__(self, max):
        self.MAX_LOCAL_LINKS = max
        self.localLinks = 0
        self.linkCacheDict = {} # Used for lookup
        self.linkCacheList = [] # Used for FIFO
        
    def hasLink(self, link):
        if link.getFullUrl() in self.linkCacheDict:
            return True

        return False

    def addLink(self, link):
        if self.localLinks == self.MAX_LOCAL_LINKS:
            evictedLink = self.linkCacheList.pop(0)
            self.linkCacheDict[evictedLink.getFullUrl()] = None
        else:
            self.localLinks = self.localLinks + 1

        # Add link to cache using the url as key, and the link as value
        self.linkCacheDict[link.getFullUrl()] = link
        self.linkCacheList.append(link)
        

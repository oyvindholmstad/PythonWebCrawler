# -*- coding: utf-8 -*-

from urlparse import urlparse

class Link(object):
    """Link"""
    def __init__(self):
        self.domain = ''
        self.path = ''
    
    @classmethod
    def linkFromDomainAndPath(cls, domain, path):
        link = Link()
        link.domain = domain
        link.path = path
        return link
        
    @classmethod
    def linkFromUrl(cls, url):
        
        domain = ""
        path = ""
        
        newlink = urlparse(url)
        
        if newlink.netloc == "":
            return None
        else:
            domain = newlink.netloc
        
        path = newlink.path
        
        if newlink.query != "":
            path = path + "?" + newlink.query
        
        if path.startswith("#"):
            return None
                
        link = Link()
        link.domain = domain
        link.path = path
        return link
    
    def getDomain(self):
        return self.domain
    
    def getPath(self):
        return self.path
        
    def getFullUrl(self):
        return "http://" + self.domain + self.path
    
    def __str__(self):
        return "<Link object> " + self.getFullUrl()
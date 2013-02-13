# -*- coding: utf-8 -*-

import urllib2, robotparser
from urlparse import urlparse
from Link import Link
        
class LinkFinder(object):
    '''LinkFinder searches for links based on the input of other links'''
    def __init__(self):
        self.robotsDict = {} # Used to keep track of robot.txts

    def findLinks(self, originatingLink):
        try:
            if self.canFetch(originatingLink):
                webPageData = self.getWebPageData(originatingLink)
                stringLinks = self.getStringLinks(webPageData)
                links = self.getLinksFromStringLinks(originatingLink, stringLinks)

                return links
        except Exception, e:
            print e
            
        return []

    def getWebPageData(self, link):
        url = link.getFullUrl()
        try:
            f = urllib2.urlopen(url)
            data = f.read()
            return data
        except Exception, e:
            raise e


    def getStringLinks(self, data):
        stringLinks = []
        start_idx = 0
    
        while (True):
            # Search for anchor tags, store location 
            anchor_idx = data.find('<a', start_idx)
            if anchor_idx == -1:
                break
            
            href_idx = data.find('href="', anchor_idx)
            if href_idx == -1:
                start_idx = anchor_idx + 5
                continue
        
            # Find url location in vicinity of anchor tag
            startquote_idx = href_idx+5
            endquote_idx = data.find('"', startquote_idx+1)
            
            # Extract url
            stringLink = unicode(data[startquote_idx+1: endquote_idx])
            stringLinks.append(stringLink)
        
            start_idx = endquote_idx
        
        return stringLinks
    
    def getLinksFromStringLinks(self, originatingLink, stringLinks):
        links = []
    
        for stringLink in stringLinks:
            link = self.getLinkFromStringLink(originatingLink, stringLink)
            if link is not None:
                links.append(link)

        return links
    
    def getLinkFromStringLink(self, originatingLink, stringLink):
        domain = ""
        path = ""
        
        newlink = urlparse(stringLink)
        
        # If the link does not contain a domain, we use the domain of the originating link
        if newlink.netloc == "":
            domain = originatingLink.domain
        else:
            domain = newlink.netloc
        
        path = newlink.path
        
        # Add arguments to path, if found
        if newlink.query != "":
            path = path + "?" + newlink.query
        
        # Anchors within same document and relative links are ignored
        if path.startswith("#"):
            return None
        elif path.startswith(".."):
            return None
        
        # Create a link object        
        link = Link.linkFromDomainAndPath(domain, path)

        return link
    
    def canFetch(self, link):
        ''' Checks with robots.txt wether we can crawl the link or not '''
        if link.getDomain() in self.robotsDict:
            rp = self.robotsDict[link.getDomain()]
            if rp == None:
                return True
            else:
                return rp.can_fetch("*", link.getFullUrl())
        else:
            print 'fetching robots.txt for ', link.getDomain()
            
            rp = robotparser.RobotFileParser()
            rp.set_url("http://"+link.getDomain()+"/robots.txt")
            try:
                rp.read()
                self.robotsDict[link.getDomain()] = rp
                return rp.can_fetch("*", link.getDomain())
            except Exception, e:
                self.robotsDict[link.getDomain()] = None
                return True              

        
def main():
    startLink = Link.linkFromUrl("http://www.telenor.com")
    lf = LinkFinder()
    links = lf.findLinks(startLink)

    for l in links:
        print l
                    
if __name__ == '__main__':
    main()      

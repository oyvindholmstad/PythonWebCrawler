# -*- coding: utf-8 -*-

import Pyro4
import time, sys
from LinkFinder import LinkFinder
from LinkCache import LinkCache

class CrawlingClientMain(object):
    """CrawlingClientMain crawls web pages and submits the unique results to the Aggregator"""
    MAX_NUMBER_OF_LINKS_IN_CACHE = 10000
    
    def __init__(self):
        self.linkFinder = LinkFinder()
        self.linkStorage = Pyro4.Proxy("PYRONAME:linkStorage")
        self.linkCache = LinkCache(CrawlingClientMain.MAX_NUMBER_OF_LINKS_IN_CACHE) # Visisted links

    def run(self):
        print 'Starting client'
        numberOfLinksToFetch = 5
        while True:
            freshLinks = []
            
            unvisitedLinks = self.linkStorage.getUnvisitedLinks(numberOfLinksToFetch)
            
            if len(unvisitedLinks) == 0:
                if self.linkStorage.isDone():
                    sys.exit(1)
                else:
                    time.sleep(1)
            else:
                for originatingLink in unvisitedLinks:
                    links = self.linkFinder.findLinks(originatingLink)
                    for link in links:
                        if not self.linkCache.hasLink(link):
                            freshLinks.append(link)
                            self.linkCache.addLink(link)
                    self.linkStorage.setLinkAsVisited(originatingLink)
            
                self.linkStorage.submitNewLinks(freshLinks)
            freshLinks = None      
          
def main():
    c = CrawlingClientMain()
    c.run()  
if __name__ == '__main__':
    main()
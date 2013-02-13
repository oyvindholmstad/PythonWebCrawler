# -*- coding: utf-8 -*-

import os, sys
from sqlite3 import *
from threading import Lock
from Link import Link

class LinkStorage(object):
    '''
    LinkStorage is used for persistent storage of Links.
    '''
    def __init__(self):
        self.database = 'tmp/storage.dat'
        self.mutex = Lock()

        if self.isFirstRun():
            self.connection = connect(self.database, check_same_thread=False)
            self.setupDatabase()
        else:
            self.connection = connect(self.database, check_same_thread=False)
        
    def isFirstRun(self):
        return not os.path.isfile(self.database)      

    def setupDatabase(self):
        print 'First run, creating tables.'
        
        # Create table for crawled links
        query = '''CREATE TABLE CrawledLinks
                            (CrawledLinkId_PK Integer PRIMARY KEY AUTOINCREMENT,
                            domain TEXT NOT NULL,
                            path TEXT, 
                            OriginLinkId int)'''
                            
        cursor=self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
        # Create table for unvisited links
        query = '''CREATE TABLE UnvisitedLinks
                            (UnvisitedLinks_PK INTEGER PRIMARY KEY AUTOINCREMENT,
                            domain TEXT NOT NULL,
                            path TEXT)'''
                            
        cursor=self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
        firstLink = Link.linkFromUrl("http://www.telenor.com")
        self.insertLink(firstLink)
        print 'Tables created.'
    
    def hasLink(self, link):
        cursor = self.connection.cursor()
        cursor.execute('SELECT 1 FROM CrawledLinks cl WHERE cl.domain == ? AND cl.path == ?', (link.getDomain(), link.getPath()))

        if cursor.fetchone():
            return True
        else:
            return False
    
    def getLinkId(self, link):
        pass
    
    def insertLink(self, link, originatingLink=None):
        self.mutex.acquire()
        
        if self.hasLink(link):
            self.mutex.release()
            return False
        print 'Storing link', link
        
        try:
            query = 'INSERT INTO CrawledLinks VALUES (null, ?, ?, ?)'
            arguments = (link.getDomain(), link.getPath(), 0)
            
            cursor = self.connection.cursor()
            cursor.execute(query, arguments)
             
            query = 'INSERT INTO UnvisitedLinks VALUES (null, ?, ?)'
            arguments = (link.getDomain(), link.getPath())
            
            cursor = self.connection.cursor()
            cursor.execute(query, arguments)

            self.connection.commit()
        except Exception, e:
            pass

        
        self.mutex.release()

        return True

    def setLinkAsVisited(self, link):
        self.mutex.acquire()
        try:
            query = 'DELETE FROM UnvisitedLinks WHERE domain=? AND path=?'
            arguments = (link.domain, link.path)

            cursor = self.connection.cursor()
            cursor.execute(query, arguments)
            self.connection.commit()
        except Exception, e:
            pass
 
        self.mutex.release()
    
    def getUnvisitedLinks(self, num):
        self.mutex.acquire()
        links = []
        domain_index = 1
        path_index = 2
        
        try:
            query = 'SELECT * FROM UnvisitedLinks LIMIT ?'
            arguments = (num,)
                        
            cursor = self.connection.cursor()
            cursor.execute(query, arguments)
            allentries = cursor.fetchall()
        
            for row in allentries:
                domain = str(row[domain_index])
                path = str(row[path_index])
                link = Link.linkFromDomainAndPath(domain, path)
                links.append(link)
        except Exception, e:
            pass
            
        self.mutex.release()
        return links

    def getVisitedLinks(self, num):
        self.mutex.acquire()
        links = []
        domain_index = 1
        path_index = 2
        
        try:
            query = 'SELECT * FROM CrawledLinks EXCEPT (SELECT * FROM UnvisitedLinks) LIMIT ?'
            arguments = (num,)
            
            cursor = self.connection.cursor()
            cursor.execute(query, arguments)
            allentries = cursor.fetchall()

            for row in allentries:
                domain = str(row[domain_index])
                path = str(row[path_index])
                link = Link.linkFromDomainAndPath(domain, path)
                links.append(link)
        except Exception, e:
            pass

        self.mutex.release()
        return links
                
    def printAllLinks(self):
        self.mutex.acquire()
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM CrawledLinks')
        allentries = cursor.fetchall()
        self.mutex.release()
        for row in allentries:
            print row
    
    def printAllUnvisitedLinks(self):
        self.mutex.acquire()
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM UnvisitedLinks')
        allentries = cursor.fetchall()
        self.mutex.release()
        for row in allentries:
            print row        
        
def main():
    ls = LinkStorage()
    ls.printAllLinks()
    
if __name__ == '__main__':
    main()
        
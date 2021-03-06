#***************************************************************************
#
#  File: database.py (sapphire.managers)
#  Date created: 05/29/2018
#  Date edited: 07/28/2018
#
#  Author: Nathan Martindale
#  Copyright © 2018 Digital Warrior Labs
#
#  Description: An interface for interacting with a mysql database
#
#***************************************************************************

import MySQLdb

import sapphire.utility
from sapphire.article import Article

class DatabaseManager:

    IDENTIFIER = "Database"

    def __init__(self):
        self.connect()
        tablesExist = self.tableCheck()
        if not tablesExist: self.createTables()

    def __del__(self):
        try: self.db.close()
        except: pass

    def connect(self):
        self.log("Connecting to database...")
        self.db = MySQLdb.connect(host=sapphire.utility.db_host, user=sapphire.utility.db_user, passwd=sapphire.utility.db_password, db=sapphire.utility.db_db)
        self.db.set_character_set('utf8')
        self.cur = self.db.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.log("Connection established")

    def tableCheck(self):
        self.log("Checking tables...")
        sql = '''SELECT 1 FROM Articles LIMIT 1;'''
        
        try: self.cur.execute(sql)
        except: 
            self.log("Database tables don't exist", "WARNING")
            return False
        return True

    def createTables(self):
        self.log("Creating tables...")
        sql = '''CREATE TABLE Articles (
            UUID char(32) primary key,
            title varchar(256),
            description text,
            timestamp datetime,
            link varchar(256),
            source_name varchar(30),
            source_type varchar(10),
            source_sub varchar(30),
            source_explicit varchar(256),
            meta_scrape_time datetime,
            meta_scrape_identifier varchar(40),
            content text,
            content_scrape_time datetime,
            content_scrape_identifier varchar(40)
        );'''
        self.cur.execute(sql)
        
        result = self.tableCheck()
        if not result: self.log("Tables couldn't be created", "ERROR")
        else: self.log("Tables successfully created!")

    def storeMetadataFrame(self, frame):
        self.log("Storing metadata frame...")
        for index, row in frame.iterrows():
            
            # make sure article with this title doesn't exist yet
            checkQuery = '''SELECT COUNT(*) FROM Articles WHERE UUID = %s'''
            self.cur.execute(checkQuery, (row['UUID'],))
            if self.cur.fetchone()[0] > 0: continue 

            insertQuery = '''INSERT INTO Articles (UUID, title, description, timestamp, link, source_name, source_type, source_sub, source_explicit, meta_scrape_time, meta_scrape_identifier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            self.cur.execute(insertQuery, (row['UUID'], row['title'], row['description'], row['timestamp'], row['link'], row['source_name'], row['source_type'], row['source_sub'], row['source_explicit'], row['meta_scrape_time'], row['meta_scrape_identifier']))

        self.db.commit()
        self.log("All new metadata stored")
        self.log("Database now contains " + str(self.getArticleCount()) + " entries")

    def getArticleCount(self):
        self.cur.execute('''SELECT COUNT(*) FROM Articles''')
        return self.cur.fetchone()[0]

    def updateArticle(self, article):
        self.log("Updating article " + article.UUID + "...")
        updateQuery = '''UPDATE Articles SET 
            title = %s,
            description = %s,
            timestamp = %s,
            link = %s,
            source_name = %s,
            source_type = %s,
            source_sub = %s,
            source_explicit = %s,
            meta_scrape_time = %s,
            meta_scrape_identifier = %s,
            content = %s,
            content_scrape_time = %s,
            content_scrape_identifier = %s
            
            WHERE UUID = %s'''

        self.cur.execute(updateQuery, (article.title, article.description, article.timestamp, article.link, article.source_name, article.source_type, article.source_sub, article.source_explicit, article.meta_scrape_time, article.meta_scrape_identifier, article.content, article.content_scrape_time, article.content_scrape_identifier, article.UUID))
        self.db.commit()
        self.log("Article updated in database")
    
    def getLackingArticleCount(self):
        findQuery = '''SELECT COUNT(*) FROM Articles WHERE content IS NULL''' 
        self.cur.execute(findQuery)
        count = self.cur.fetchone()[0]
        return count

    # NOTE: returns first article without content
    def getFirstLackingArticle(self):
        if self.getLackingArticleCount() == 0: return False
        
        findQuery = '''SELECT * FROM Articles WHERE content IS NULL LIMIT 1''' 
        self.cur.execute(findQuery)
        article_row = self.cur.fetchone()
        article = Article()
        article.populateFromRow(article_row)
        return article
    
    def getRecentLackingArticle(self):
        if self.getLackingArticleCount() == 0: return False
        
        findQuery = '''SELECT * FROM Articles WHERE content IS NULL ORDER BY timestamp DESC LIMIT 1''' 
        self.cur.execute(findQuery)
        article_row = self.cur.fetchone()
        article = Article()
        article.populateFromRow(article_row)
        return article
    
    def log(self, msg, channel=""):
        sapphire.utility.logging.log(msg, channel, source=self.IDENTIFIER)

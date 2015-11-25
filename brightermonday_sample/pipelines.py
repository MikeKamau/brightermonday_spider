# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
from scrapy.exceptions import DropItem
from scrapy.http import Request


class BrightermondaySamplePipeline(object):
	def __init__(self):
		try:
			self.conn = MySQLdb.connect(user='root', passwd='', db='jobs', host='localhost', charset='utf8', use_unicode=True)
			self.cursor = self.conn.cursor()
		except MySQLdb.Error, e:
			print "Error %d: %s" %(e.args[0], e.args[1])
		
	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO majob (title, description, link) VALUES (%s, %s, %s)""",
				(item['title'].encode('utf-8'),
				item['desc'].encode('utf-8'),
				item['link'].encode('utf-8')))
        		
			self.conn.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s" %(e.args[0], e.args[1])
		  		
		return item
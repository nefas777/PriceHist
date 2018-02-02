# -*- coding: utf-8 -*-
import requests
import re
from lxml import html

class myException(Exception):
	def __init__(self, message):
		super(myException, self).__init__(message)


class Prod():
	def __init__(self, vendor, name, goodid, price, link):
			self.name = name
			self.vendor = vendor
			self.goodid = goodid
			self.price = price
			self.link = link
			
	def __repr__(self):
		return self.vendor + '\t' + self.name + '\t' + str(self.price)
		
	def UlGetPar(self):
		r = requests.get(self.link)
		tree = html.fromstring(r.text)
		title = tree.xpath('//ul[contains(@class, "b-dotted-line-list")]//span[@class="b-dotted-line__title"]')
		title = [r.text_content().strip().upper() for r in title]
		content = tree.xpath('//ul[contains(@class, "b-dotted-line-list")]//div[@class="b-dotted-line__content"]')
		content = [r.text_content().strip().upper() for r in content]
		data = {}
		self.diag = None
		self.wifi = None
		for i in range(len(title)):
			if 'ДИАГОНАЛ' in title[i]:
				self.diag = content[i]
			elif 'WI-FI' in title[i]:
				self.wifi = content[i]
			else:
				data[title[i]] = content[i]
				
		self.info = data
		
	def checkInDB(self, cursor, table):
		cursor.execute('select * from '+table+' where goodid = '+str(self.goodid))
		d = []
		for r in cursor:
			d.append(r)
		if len(d) == 0:
			return False
		elif len(d) == 1:
			return True
		else:
			raise myException('duplicated product '+ str(self.goodid) + ' in '+table)
	
	def checkHasInfo(self, cursor, table):
		'''Before executing this func check if self in DB (checkInDB is True)'''
		cursor.execute('select info from '+table+' where goodid = '+str(self.goodid))
		d=[]
		for r in cursor:
			d.append(r[0])
		if d[0] is None:
			return False
		return True
		
	def inesrtDB(self, cnx, cursor, table):
		if self.checkInDB(cursor, table):
			cursor.execute(('insert into '+ table + '(goodid, vendor, name) values (%s, %s, %s)'), (self.goodid, self.vendor, self.name))
		cursor.execute('insert into')
	
class Ulmart(list):
	def GetProd(self, url, pages = 1, **kwargs):
		trouble = []
		for pageNum in range(pages):
			kwargs['pageNum'] = pageNum + 1
			r = requests.get(url, params = kwargs)
			tree = html.fromstring(r.text)
			a = tree.xpath('//div[@class="b-products__body"]//section[contains(@class, "b-product")]//div[contains(@class, "b-product-status")]//span')
			for p in a:
				name = p.get('data-gtm-eventproductname').upper()
				vendor = p.get('data-gtm-eventvendorname').upper()
				goodid = int(p.get('data-avail-goodid'))
				price = float(p.get('data-gtm-eventproductprice'))
				link = 'https://www.ulmart.ru'+tree.xpath('//*[@id="linkText'+ str(goodid)+'"]')[0].get('href')
				if vendor in name:
					name = name.split(vendor)[1].strip()
					pr = Prod(name=name, vendor=vendor, goodid=goodid, price=price, link = link)
				else:
					print("No vendor in name in "+str(goodid))
					pr = Prod(name=name, vendor=vendor, goodid=goodid, price=price, link = link)
					trouble.append(pr)
				self.append(pr)
		return trouble
	
	def UlGetPar(self, cnx, cursor, table):
		for p in self:
			cursor.execute('select info from '+table+' where goodid='+str(p.goodid) + ';')
			d=[]
			for r in cursor:
				d.append[r[0]]
			if len(d) == 0:

			elif len(d) == 
P = Ulmart()
t = P.GetProd(url = r'https://www.ulmart.ru/catalog/tvs', pages=7)                


	
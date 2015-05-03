import csv
import ssl
from urlparse import urlparse
from bs4 import BeautifulSoup
import ssl
import urllib
import urllib2
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


def scrape(ur):
	try:
		json_item = {}	
		html = urllib.urlopen(ur).read()
		soup = BeautifulSoup(html)

		title = soup.find('h1',itemprop="name")
		saddress = soup.find('span',itemprop="streetAddress")
		postalcode = soup.find('span',itemprop="postalCode")
		rating  = soup.find('meta',{"itemprop":"ratingValue"})['content']
		#print title.text
		json_item["name"]=title.text
		#print saddress.text
		json_item["address"]=saddress.text
		#print postalcode.text
		json_item["postalCode"]=postalcode.text
		#print rating
		json_item["rating"]=rating
		#print "-------------------"
		return json_item
	except:
		pass	
		return json_item


f = open('/home/aditya/Downloads/DOHMH.csv')
csv_f = csv.reader(f)
rname = "india"
rplace = "brooklyn"
urllist = []
rlist = []
r_complete = []
count = 0
json_data = {}

for row in csv_f:
 		if ((rname.lower() in row[1].lower()) and (rplace.lower() in row[2].lower())):
  			rlist.append(str(row[1] + "," +row[2] + ":" + row[10] + ":" + str(row[13].split(","))))

f.close()

for item in rlist:
	json_item = {}
	item = item.split(":")
	flag = False
	page = urllib2.urlopen('http://www.bing.com/search?q='+item[0].replace(' ','+'),context=gcontext)
	soup = BeautifulSoup(page)
	for anchor in soup.findAll('a', href=True):
		#print anchor['href']
		if(anchor["href"].startswith("http://www.yelp.com/biz/")):
			print anchor["href"]
			json_item = scrape(anchor["href"])
			
			item[1] = item[1].split(',')
			
			score = item[2]
			sum = 0
			t2 = item[2]
			item[2] = t2[1:-1].split(",")
			for eachitem in item[2]:
				t2 = eachitem.strip()
				num = t2[1:-1].strip()
				sum = sum + int(num)				
		
			json_item["Violation_Score"] = sum
			json_item["Violation_Code"] = item[1]
			print json_item
 			break




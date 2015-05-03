import urllib
from bs4 import BeautifulSoup
import re
from threading import Thread
 
#List of yelp urls to scrape
url=['http://www.yelp.com/biz/villabate-alba-brooklyn']
 
i=0
#function that will do actual scraping job
def scrape(ur):
 
     html = urllib.urlopen(ur).read()
     soup = BeautifulSoup(html)

     title = soup.find('h1',itemprop="name")
     saddress = soup.find('span',itemprop="streetAddress")
     postalcode = soup.find('span',itemprop="postalCode")
     rating  = soup.find('meta',{"itemprop":"ratingValue"})['content']
     print title.text
     print saddress.text
     print postalcode.text
     print rating
     print "-------------------"
 
threadlist = []
 
#making threads
while i<len(url):
          t = Thread(target=scrape,args=(url[i],))
          t.start()
          threadlist.append(t)
          i=i+1
 
for b in threadlist:
          b.join()
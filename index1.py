import csv
import urllib2
import os
from urlparse import urlparse
import re 
import math
import operator
import gzip
from StringIO import StringIO
import parser
from operator import itemgetter



included_rows = []
zippedlist = []
f = open('/home/aditya/Downloads/DOHMH.csv')
csv_f = csv.reader(f)
	  
print (os.getcwd())

#t = open('/home/aditya/web/project/rest_index.txt','r+')
for row in csv_f:
	included_rows.append(row)	
f.close()


t = open('/home/aditya/web/project/rest_index.txt','r+')
for item in included_rows:
	t.write(str(item))
	print item[0]
t.close()



																																																																											

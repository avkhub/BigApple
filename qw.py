from itertools import groupby
from operator import itemgetter
import csv
import os



included_rows = []
zippedlist = []
f = open('/home/aditya/Downloads/DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
next(f)
csv_f = csv.reader(f)
	  
print (os.getcwd())

t = open('/home/aditya/web/project/rest_index.txt','r+')
for row in csv_f:
	included_rows.append(row)	
	t.write(str(row))
f.close()
t.close()


# load the data and make sure it is sorted by the first column
sortby_key = itemgetter(0)

f = open("/home/aditya/web/project/rest_index.txt", "r")
page = f.read() 
page = page.split(']')
for line in page:
	print line
f.close(); 

'''data = (map(int, line.split(',')) for line in open('/home/aditya/web/project/rest_index.txt'))
              

# group by the first column
grouped_data = []
for key, group in groupby(data, key=sortby_key):
    assert key == len(grouped_data) # assume the first column is 0,1, ...
    grouped_data.append([trio[1:] for trio in group])

# print the data
for i, pairs in enumerate(grouped_data):
    print i, pairs'''
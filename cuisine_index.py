import csv

f = open('/home/aditya/Downloads/DOHMH.csv')
csv_f = csv.reader(f)
country_list = ["american"]
c_cuisine = []
count = 0


for row in csv_f:
 		if any(s in row[7].lower() for s in country_list):
  			c_cuisine.append(row)		
f.close()

with open('/home/aditya/Downloads/country_cuisine.csv' , 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter= ',')
	for item in c_cuisine:
		writer.writerow(item)

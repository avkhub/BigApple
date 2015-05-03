from flask import Flask
from flask import request
from flask import jsonify
from difflib import SequenceMatcher
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import os
import json
import csv
import socket
import sys
from urlparse import urlparse
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Newyork, NY'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = "YyxPpfcHzWoMafYXCxMNew"
CONSUMER_SECRET = "Y_4w9viUCaJB0DSpJKgkbD4dqOk"
TOKEN = "yZ1weFpd9FAk-5Ej8jilKuMGvK6v6-7j"
TOKEN_SECRET = "U9hpSGKWyoPjKTtTt34I-8qJw7Y"

def similar(a,b):
	return SequenceMatcher(None, a , b).ratio()




def request(host, path, url_params=None):

	"""Prepares OAuth authentication and sends the request to the API.
	Args:
	host (str): The domain host of the API.
	path (str): The path of the API after the domain.
	url_params (dict): An optional set of query parameters in the request.
	Returns:
	dict: The JSON response from the request.
	Raises:
	urllib2.HTTPError: An error occurs from the HTTP request."""


	url_params = url_params or {}
	url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))
	consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
	oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)
	oauth_request.update(
	{
	'oauth_nonce': oauth2.generate_nonce(),
	'oauth_timestamp': oauth2.generate_timestamp(),
	'oauth_token': TOKEN,
	'oauth_consumer_key': CONSUMER_KEY
	}
	)
	token = oauth2.Token(TOKEN, TOKEN_SECRET)
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
	signed_url = oauth_request.to_url()
	print signed_url
	print u'Querying {0} ...'.format(url)
	conn = urllib2.urlopen(signed_url, None)
	try:
	 response = json.loads(conn.read())
	finally:
	 conn.close()
	return response


def search(lat , lon):
	"""Query the Search API by a search term and location.
	Args:
	term (str): The search term passed to the API.
	location (str): The search location passed to the API.
	Returns:
	dict: The JSON response from the request.
	"""
	url_params = {
	#'term': term.replace(' ', '+'),
	#'location': location.replace(' ', '+'),
	'll': lat + "," + lon,
	#'category':"american", 
	#'name' : "villabate alba",
	'limit': SEARCH_LIMIT
	
	}
	print (url_params)
	return request(API_HOST, SEARCH_PATH, url_params=url_params)



def get_business(business_id):
	"""Query the Business API by a business ID.
	Args:
	business_id (str): The ID of the business to query.
	Returns:
	dict: The JSON response from the request.
	"""
	business_path = BUSINESS_PATH + business_id
	return request(API_HOST, business_path)
def query_api(lat,lon,csv_f):
	"""Queries the API by the input values from the user.
	Args:
	term (str): The search term to query.
	location (str): The location of the business to query.
	"""
	
	response = search(lat,lon)
	businesses = response.get('businesses')
	
	
	if not businesses:
	 print u'No businesses for {0} in {1} found.'.format(term, location)
	 return 	

	'''business_id = businesses[0]['id']
	print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(len(businesses),
	business_id)
	response = get_business(business_id)
	print u'Result for business "{0}" found:'.format(business_id)
	pprint.pprint(response, indent=2)
	print ((businesses[0]['location']['address']))'''
	included_rows = []
	for row in csv_f:
		included_rows.append(row)
		filter_b = []
	for item in businesses:
	  try:
		phone = item['phone']
		pincode = item['location']['postal_code']
		door_num = item['location']['address'][0].split()[0]
		boro = item['location']['address'][0].split()[1]
		name = item['name']
		categories = item["categories"]
		c_list = ["halal","bars" , "french","afghani","afghani","newamerican","American","arabian","argentine","vietnamese","british","belgian","buffets","burgers","cafes","cafeteria","chinese","diners","german","indpak","irish","italian","japanese","pakistani","seafood","spanish","vegetarian","mideastern","mediterranean","hotdog","foodstands","caribbean","greek","soup","steak"]
		flag_cat = False
		for key,value in categories:
			 if (value in c_list):
			 	print value
				flag_cat = True
		score = 0
		violation_code = []
		name_s = name
		boro_s = boro
		for row in included_rows:
			
			if((pincode == row[5]) and (door_num == row[3]) and (flag_cat) == True):					
				
			   	 #similarity = SequenceMatcher(None,name,row[1]).ratio()
				 if((row[1].split()[0].lower() in name_s.lower() )==True):
					print flag_cat		 	
				 	violation_code = row[10]
				 	#calculating violation score
				 	print violation_code
					score_list = row[13].split(',')
					#print score_list
					for item_s in score_list:
						score = score + int(item_s)
					violation_code = violation_code.split(',')
					item['violation_score'] = score
					item['violation_codes'] = violation_code
		#print item
					filter_b.append(item)
	  except:
		pass
	with open(os.getcwd()+"/yelptop20"+".txt" , "r+") as outfile:
		json.dump(businesses,outfile,indent = 2)

	return filter_b


def scrape(ur):
	try:

		json_item = {}	
		html = urllib.urlopen(ur).read()
		soup = BeautifulSoup(html)
		
		title = soup.find('h1',itemprop="name")
		saddress = soup.find('span',itemprop="streetAddress")
		postalcode = soup.find('span',itemprop="postalCode")
		phone = soup.find('span', itemprop='telephone')
		price = soup.find('span', itemprop='priceRange')
		try:
			rating  = soup.find('meta',{"itemprop":"ratingValue"})['content']
			#print title.text
		except:
			pass
		json_item["name"]=title.text		
		json_item["address"]=saddress.text		
		json_item["postalCode"]=postalcode.text		
		json_item["rating"]=rating
		json_item["phone"] = phone.text
		json_item['price'] = price.text

		
		return json_item
	except:
		pass


app = Flask(__name__)

@app.route("/location/<lat>/<lon>")


def main(lat = None , lon = None):
	
	
	#print lat 
	#print lon
	#print lon
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
	parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
	input_values = parser.parse_args()
	try:
 #print (input_values.term, input_values.location)
 		f = open('/home/aditya/Downloads/DOHMH.csv')
 		csv_f = csv.reader(f)
 		out_onpage = query_api(lat,lon,csv_f)
 		return jsonify(results=out_onpage)
	except urllib2.HTTPError as error:
 		sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


@app.route("/cuisine/<cname>/<cloc>")

def cuisine(cname = None , cloc = None):
	#gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	f = open('/home/aditya/Downloads/DOHMH.csv')
	csv_f = csv.reader(f)
	rname = cname
	rplace = cloc
	urllist = []
	rlist = []
	r_complete = []
	
	json_data = {}

	for row in csv_f:
 		if ((rname.lower() in row[1].lower()) and (rplace.lower() in row[2].lower())):
  			rlist.append(str(row[1] + "," +row[2] + ":" + row[10] + ":" + str(row[13].split(","))))

	f.close()
	count = 0
	for item in rlist:
		json_item = {}
		item = item.split(":")
		flag = False
		page = urllib2.urlopen('http://www.bing.com/search?q='+item[0].replace(' ','+'))
		soup = BeautifulSoup(page)
			
		for anchor in soup.findAll('a', href=True):
			#print anchor['href']
			try:
				
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
					count = count + 1
					print count
					json_data[count] = json_item
					break
			except:
				pass


	return jsonify(results=json_data)
 				
		


if __name__ == "__main__":
    app.run(debug = True)
    
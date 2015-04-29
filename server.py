from flask import Flask
from flask import jsonify
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

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Newyork, NY'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'
# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = "YyxPpfcHzWoMafYXCxMNew"
CONSUMER_SECRET = "Y_4w9viUCaJB0DSpJKgkbD4dqOk"
TOKEN = "yZ1weFpd9FAk-5Ej8jilKuMGvK6v6-7j"
TOKEN_SECRET = "U9hpSGKWyoPjKTtTt34I-8qJw7Y"

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


def search():
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
	'll':"40.693911"+ "," + "-73.986375",
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
def query_api(csv_f):
	"""Queries the API by the input values from the user.
	Args:
	term (str): The search term to query.
	location (str): The location of the business to query.
	"""
	lon = None
	response = search()
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
	for item in businesses:
	  try:
		phone = item['phone']
		pincode = item['location']['postal_code']
		door_num = item['location']['address'][0].split()[0]
		score = 0
		violation_code = []
		#violation_codes = [] 
		for row in included_rows:
			
			if ((phone == row[6]) and (pincode == row[5]) and (door_num == row[3])):	
				#print row[13]
				violation_code = row[10]
				print violation_code
				#calculating violation score

				score_list = row[13].split(',')
				#print score_list
				for item_s in score_list:
					score = score + int(item_s)
				violation_code = violation_code.split(',')
		item['violation_score'] = score
		item['violation_codes'] = violation_code
		#print item
	  except:
		pass
	with open(os.getcwd()+"/yelptop20"+".txt" , "r+") as outfile:
		json.dump(businesses,outfile,indent = 2)

	return businesses




app = Flask(__name__)

@app.route("/")


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
	parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
	input_values = parser.parse_args()
	try:
 #print (input_values.term, input_values.location)
 		f = open('/home/aditya/Downloads/DOHMH.csv')
 		csv_f = csv.reader(f)
 		out_onpage = query_api(csv_f)
 		return jsonify(results=out_onpage)
	except urllib2.HTTPError as error:
 		sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

 	

if __name__ == "__main__":
    app.run(debug = True)
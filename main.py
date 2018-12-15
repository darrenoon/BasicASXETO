from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from contextlib import closing
from requests import get
import webapp2 as webapp
# from dateutil import parser
import datetime
import numpy as np
# import scipy.stats as si
import math

def Output(input):
# should output to file on google cloud storage??
	print(input)

def simple_get(url):
	"""
	Attempts to get the content at url by making an HTTP GET request.
	If the content-type of response is some kind of HTML/XML, return the
	text content, otherwise return None.
	"""
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None

	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None

def is_good_response(resp):
	"""
	Returns True if the response seems to be HTML, False otherwise.
	"""
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

import sys
def log_error(e):
	"""
	It is always a good idea to log errors.
	This function just prints them, but you can
	make it do anything.
	"""
	print(e)

def get_options_prices_asx(input_code):		
	input_url = "https://www.asx.com.au/asx/markets/optionPrices.do?by=underlyingCode&underlyingCode=" + input_code + "&expiryDate=&optionType=B"

	raw_html = simple_get(input_url)
	html = BeautifulSoup(raw_html, 'html.parser')

	OptionPriceOutput = ""

	for i, li in enumerate(html.select('tr')):

		ParseText = li.text
		ParseText = ParseText.replace('\n\t\t\t\t',"")
		ParseText = ParseText.replace('\n',"",1)
		ParseText = ParseText.replace(',',"")
		ParseText = ParseText.replace('\n',",")

		if "Code," not in ParseText:
			if "Options," not in ParseText:
				# global OptionPriceOutput
				OptionPriceOutput += ParseText + '<br>'

	return OptionPriceOutput




class HelloWebapp(webapp.RequestHandler):
	def get(self):
		t = get_options_prices_asx("bhp")
		self.response.write("<br>******<br>")
		self.response.write(t)
		t = get_options_prices_asx("xjo")
		self.response.write("<br>******<br>")
		self.response.write(t)

class GetFromUrl(webapp.RequestHandler):
	def get(self, input_code):
		t = get_options_prices_asx(input_code)
		self.response.write("<br>******<br>")
		self.response.write(t)		

app = webapp.WSGIApplication([
    ('/(\w+)', GetFromUrl),	
    ('/', HelloWebapp),	
], debug=True)

# print(log_error('abc'))

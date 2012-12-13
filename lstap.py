#!/usr/bin/env python2

import argparse
import codecs
import re
import sys
import urllib
from datetime import datetime, date
from BeautifulSoup import BeautifulSoup

def convert_entities(s):
	return BeautifulSoup(s, convertEntities=BeautifulSoup.HTML_ENTITIES).getText()

def parse_beer(b):
	info = {}

	date = b.find('sub', {'class': 'listed-on'}).string
	info['date'] = datetime.strptime(date, 'Listed on %b %d, %Y').date()
	info['brewery'] = convert_entities(b.find('h4').string)
	info['beer'] = convert_entities(b.find('h2', {'class': 'beer-name'}).string)
	return info

def parse(soup):
	info = []
	tap_list = soup.find('div', {'id': 'desktop-tap-list'})
	beers = tap_list.findAll('div', {'id': re.compile("beer-[0-9]+")})
	for beer in beers:
		info.append(parse_beer(beer))
	return info

def snarf_url(url):
	return urllib.urlopen(url)

def filter_none(beer):
	return True

def filter_today(beer):
	return beer['date'] == date.today()

def print_default(beer):
	print "%s - %s" % (beer['brewery'], beer['beer'])

def print_verbose(beer):
	print "[%s] %s - %s" % (beer['date'], beer['brewery'], beer['beer'])

def key_date(beer):
	return beer['date']

def key_brewery(beer):
	return beer['brewery']

if __name__ == '__main__':
	sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

	parser = argparse.ArgumentParser(description='List beers on Taplister')
	parser.add_argument('url', type=str,
			    help='Taplister URL for the bar')
	parser.add_argument('--today', dest='filter', action='store_const',
			    const=filter_today, default=filter_none,
			    help='Show only beers listed today')
	parser.add_argument('--verbose', dest='display', action='store_const',
			    const=print_verbose, default=print_default,
			    help='Print all information about the beer')
	parser.add_argument('--date', dest='sort_key', action='store_const',
			    const=key_date, default=key_brewery,
			    help='Sort beers by date instead of brewery')

	args = parser.parse_args()

	p = snarf_url(args.url)
	soup = BeautifulSoup(p, convertEntities=BeautifulSoup.HTML_ENTITIES)

	map(args.display,
		sorted([b for b in parse(soup) if args.filter(b)], key=args.sort_key))


#!/usr/bin/env python2

import re
import pprint
from datetime import datetime
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


def parse_beers(soup):
	info = []
	tap_list = soup.find('div', {'id': 'desktop-tap-list'})
	beers = tap_list.findAll('div', {'id': re.compile("beer-[0-9]+")})
	for beer in beers:
		info.append(parse_beer(beer))
	return info

def snarf_url(url):
	pass

def snarf_file(name):
	f = open(name, 'r')
	return f.read()


if __name__ == '__main__':
	p = snarf_file("./test/dh.html")
	soup = BeautifulSoup(p, convertEntities=BeautifulSoup.HTML_ENTITIES)

	beer = parse_beers(soup)
	pprint.pprint(beer)

#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
description
'''

# MODULES

import os
import string
from get_reblog_urls import get_reblog_urls
from take_screenshot import Screenshot

# VARIABLES

# tumblr post url
my_source_url = "http://nasahistory.tumblr.com/post/111965945471/the-discovery-on-her-final-flight"

# screenshot size
my_width = 800
my_height = 1000

# max amount of reblog pages
max_pages = 1

# speed

# FUNCTIONS

def validate(my_string):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	my_string = my_string.replace("/", "_")
	my_string.join(c for c in my_string if c in valid_chars)
	return my_string

def main(url):
	# get permalinks
	urls = get_reblog_urls(url, max_pages)

	# create and go into folder
	directory = url
	directory = validate(directory)
	if not os.path.exists(directory):
		os.makedirs(directory)
	os.chdir(directory)

	# create screenshot folder
	if not os.path.exists('screenshots'):
		os.makedirs('screenshots')
	os.chdir('screenshots')

	# take screenshots
	s = Screenshot()
	for url in urls:
		filename = validate(url) + '.png'
		s.capture(url, filename, my_width, my_height)

	# make video

	# make text file

# WORK

if __name__ == '__main__':
  print main(my_source_url)
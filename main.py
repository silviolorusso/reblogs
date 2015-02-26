#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
takes a tumblr post and produces screenshots of its reblogs

usage: python main.py [width] [height] [max_pages] [speed] [url] 
'''

# MODULES

import os
import sys
import subprocess
import string
from get_reblog_urls import get_reblog_urls
from take_screenshot import Screenshot

# VARIABLES

# tumblr post url
my_source_url = "http://nasahistory.tumblr.com/post/111965945471/the-discovery-on-her-final-flight"

# screenshot size
my_width = 500
my_height = 700

# max amount of reblog pages
my_max_pages = 1

# video speed
my_speed = "12"

# FUNCTIONS

def validate(my_string):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	my_string = my_string.replace("/", "_")
	my_string.join(c for c in my_string if c in valid_chars)
	return my_string

def main(width, height, max_pages, speed, source_url):

	# get permalinks
	urls = get_reblog_urls(source_url, max_pages)

	# make text file

	# create and go into folder
	directory = source_url
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
	i = 0
	for url in urls:
		filename = str(i).zfill(5) + '_' + validate(url) + '.png'
		#filename = str(i).zfill(5) + '.png'
		s.capture(url, filename, width, height)
		i += 1

	# make video
	# ffmpeg -f image2 -r 12 -pattern_type glob -i '*.png' -vcodec mpeg4 -y movie.mp4
	subprocess.call(["ffmpeg", "-f", "image2", "-r", "12", "-pattern_type", "glob", "-i", "*.png", "-vcodec", "mpeg4", "-y", "../movie.mp4"])
	print "\nVideo successfully saved."

# WORK

if __name__ == '__main__':
	# get arguments
	# width
	try:
		my_width = int(sys.argv[1])
	except IndexError:
		print "\nWidth not provided."
	# height
	try:
		my_height = int(sys.argv[2])
	except IndexError:
		print "\nHeight not provided."
		# height
	try:
		my_max_pages = int(sys.argv[3])
	except IndexError:
		print "\nMax notes pages not provided."
	try:
		my_speed = sys.argv[4]
	except IndexError:
		print "\nSpeed not provided."
	try:
		my_source_url = sys.argv[5]
	except IndexError:
		print "\nSource URL not provided."

	main(my_width, my_height, my_max_pages, my_speed, my_source_url)
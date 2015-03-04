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
import time
import datetime
from get_reblog_urls import get_reblog_urls
from take_screenshot import Screenshot

# VARIABLES

# tumblr post url
my_source_url = "http://nasahistory.tumblr.com/post/111965945471/the-discovery-on-her-final-flight"

# screenshot size
my_width = 500
my_height = 700

# max amount of reblog pages
my_max_pages = 5

# video speed: 1 = normal; 2 = half
my_speed = 2.5

# FUNCTIONS

def validate(my_string):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	my_string = my_string.replace("/", "_")
	my_string.join(c for c in my_string if c in valid_chars)
	return my_string

def main(width, height, max_pages, speed, source_url):

	# get permalinks
	urls = get_reblog_urls(source_url, max_pages)
	print "Amount of reblogs: " + str(len(urls))

	# all data related to video
	time_str = time.strftime("%Y%m%d-%H%M%S")
	data_str = str(width) + "_" + str(height) + "_" + str(max_pages) + "_" + speed + '_' + time_str

	# create and go into source url folder
	directory = source_url
	directory = validate(directory)
	if not os.path.exists(directory):
		os.makedirs(directory)
	os.chdir(directory)

	# make report
	urls_string = ""
	for url in urls:
		urls_string += url + "\n"
	today = datetime.date.today()
	todaystr = today.strftime('%d, %b %Y')
	report_text = '''
%s reblogs from %s - %s 

Source post: %s

Amount of reblogs: %s

Reblog URLS:
%s
	''' % (len(urls), source_url, todaystr, source_url, len(urls), urls_string)
	report_filename = "report_" + data_str + ".txt"
	report = open(report_filename, "w")
	report.write(report_text)
	report.close()

	# create screenshot folder
	directory_stamped = 'screenshots_' + data_str 
	if not os.path.exists(directory_stamped):
		os.makedirs(directory_stamped)
		os.chdir(directory_stamped)

	# take screenshots
	s = Screenshot()
	i = 0
	# for animated gifs
	delay = 0
	for url in urls:
		filename = str(i).zfill(5) + '_' + validate(url) + '.png'
		clipwidth = "--clipwidth=" + str(width)
		clipheight = "--clipheight=" + str(height)
		my_delay = "--delay=" + str(delay)
		try: 
			# use webkit2png
			subprocess.call(["webkit2png", url, "-C", "-W", str(width), "-H", str(height), clipwidth, clipheight, "--scale=1", my_delay, "-o", filename])
		except:
			# use Qt
			s.capture(url, filename, width, height)
			sleep(1)
		i += 1 
		if delay <= 3:
			# 1 frame (24fs per sec)
			delay += 0.04
		else:
			delay = 0
		print "Screenshot " + str(i) + " out of " + str(len(urls)) + " saved."

	# make video
	# ffmpeg -f image2 -pattern_type glob -i '*.png' -vf "setpts=2.5*PTS" -r 25 -vcodec mpeg4 -qscale:v 1 -y movie.mp4
	speed_arg = "setpts=" + str(speed) + "*PTS"
	movie_filename = "../movie_" + data_str + ".mp4" 
	subprocess.call(["ffmpeg", "-f", "image2", "-pattern_type", "glob", "-i", "*.png", "-vf", speed_arg, "-r", "25", "-vcodec", "mpeg4", "-qscale:v", "1", "-y", movie_filename])
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
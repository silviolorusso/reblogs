#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
get urls from tumblr
'''

# MODULES

from bs4 import BeautifulSoup
import urllib2
import re
from urlparse import urlparse
from time import sleep
from datetime import date

# VARIABLES

my_url = "http://allcapspoetry.tumblr.com/post/111030863348/afraid-the-neighbourhood"

my_max_pages = 20

# FUNCTIONS

# gets the ID of Tumblr post
def browse_notes(notes_url):
  notes_page = urllib2.urlopen(notes_url)
  notes_soup = BeautifulSoup(notes_page.read())
  more_notes_link = notes_soup.find_all("a", class_="more_notes_link")
  # get link id
  next_notes_id = re.findall("/notes/.*/.*\?from_c=(.*)'", str(notes_soup))
  if not next_notes_id:
    print 'All notes browsed.\n'
    return
  else:
    return next_notes_id[0]

# gets the urls of reblogged post
def get_urls(notes_url):
  notes_page = urllib2.urlopen(notes_url)
  notes_soup = BeautifulSoup(notes_page.read())
  spans = notes_soup.find_all("span", class_="action")
  reblog_urls = []
  for span in spans:
    reblog_url = re.findall("data-post-url=\"(.*)\"><a", str(span))
    if reblog_url:
      reblog_urls.append(reblog_url[0])
  return reblog_urls

def get_reblog_urls(source_url, max_pages):
  print "Permalink: " + source_url + "\n"
  # open permalink
  page = urllib2.urlopen(source_url)
  soup = BeautifulSoup(page.read())

  # try to get post key
  post_key = re.findall("/notes/.*/(.*)\?", str(soup))
  if not post_key:
    print "No post key. "
    return
  else:
    post_key = post_key[0]

  # get ids to browse notes (from_c)
  parsed_uri = urlparse(source_url)
  domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
  try:
    post_id = re.findall("http://.*/post/(.*)/", source_url)[0]
  except IndexError:
     post_id = re.findall("http://.*/post/(.*)", source_url)[0]   
  # tumblr permalink formatted to get notes
  notes_url_tumblr = domain + 'notes/' + post_id + '/' + post_key
  print "Permalink of Tumblr notes: " + notes_url_tumblr + "\n"
  # get ids
  next_notes_id = browse_notes(notes_url_tumblr)
  next_notes_ids = []
  i = 0
  while next_notes_id and i <= max_pages:
    next_notes_ids.append(next_notes_id)
    next_notes_id = browse_notes(notes_url_tumblr + '?from_c=' + next_notes_id)
    i += 1
    sleep(1)
  
  print 'Next notes IDs'
  print next_notes_ids

  # get notes permalinks from dashboard
  # check if it's a tumblr.com domain or a custom one
  if 'tumblr.com' in domain:
    tumblr_name = re.findall("http://(.*)\.tumblr", source_url)[0]
  else:
    if "http://www." in domain:
      tumblr_name = re.findall("http://www\.(.*)\.", source_url)[0]
    else:
      tumblr_name = re.findall("http://(.*)\.", source_url)[0]
  notes_url_dash = 'http://www.tumblr.com/dashboard/notes/' + post_id + '/' + post_key + '/' + tumblr_name
  print "Permalink of dashboard notes: " + notes_url_dash + "\n"
  # get all notes permalinks
  notes_urls_dash = [] 
  for next_notes_id in next_notes_ids:
    notes_urls_dash.append(notes_url_dash + '?from_c=' + next_notes_id)

  # get reblog permalinks 
  reblog_urls = []
  for url in notes_urls_dash:
    reblog_url = get_urls(url)
    reblog_urls.extend(reblog_url)
    sleep(1)

  # add original permalink and reorder
  reblog_urls.append(source_url)
  reblog_urls.reverse()
  return reblog_urls

# WORK

if __name__ == '__main__':
  print get_reblog_urls(my_url, my_max_pages)
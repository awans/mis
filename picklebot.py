from BeautifulSoup import BeautifulSoup
import pprint
import os
import urllib2
import re
import datetime
import helper
import pickle


def parse_title(full_title):
  # near the end of the string for something that's in parens
  # tricky case is if a post has like (blah) (loc) in the title; 
  # make sure we get the rightmost by disallowing internal parens
  loc_m = re.search(r"(\((?P<location>[^)]*)\))?\Z", full_title)
  location = loc_m.group('location')
  full_title = full_title[0:loc_m.start()]

  age_m = re.search(r"(\s\-\s)?(?P<age>\d+)?\s?\Z",full_title)
  age = age_m.group('age')
  full_title = full_title[0:age_m.start()]
  
  gen_m = re.search(r"(\s\-\s)?((?P<gone>[mwt]+)4(?P<gtwo>[mwt]+))?\s?\Z", full_title)
  me_gender = gen_m.group('gone')
  you_gender = gen_m.group('gtwo')
  title = full_title[0:gen_m.start()]
  
  return {'location':location, 'age':age, 'me_gender':me_gender, 'you_gender':you_gender, 'title':title}
  

def parse_post(post_html, post_id):
  post_soup = BeautifulSoup(post_html)
  post_dict = parse_title(post_soup.h2.string)

  post_dict['id'] = post_id
  post_dict['url'] = 'http://sfbay.craigslist.org/sfc/mis/' + post_id + '.html'

  userbody = post_soup.find(id="userbody")
  body = ''
  for node in userbody.contents:
    if not node.string:
      continue
    elif 'START CLTAGS' in node.string:
      break
    else:
      body += node.string

  post_dict['body'] = body
  return post_dict

missed_connections = []

for root, dirs, files in os.walk(helper.FOLDERNAME):
  for name in files:
    fname, ext = os.path.splitext(name)
    if ext == '.html':
      f = open(os.path.join(root, name), 'r')
      post_html = f.read()
      f.close()
    
      missed_connections.append(parse_post(post_html, fname))
    
pickle_file = open(helper.PICKLEJAR, 'w')
pickle.dump(missed_connections, pickle_file)
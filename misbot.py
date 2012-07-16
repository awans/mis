from BeautifulSoup import BeautifulSoup
import urllib2
import datetime
import helper
import re
import os.path

def parse_id(url):
  return re.search('\d{10}', url).group(0)

response = urllib2.urlopen('http://sfbay.craigslist.org/sfc/mis/')
html = response.read()
soup = BeautifulSoup(html)
all_the_post_urls = [anchor['href'] for anchor in soup.findAll('a') if anchor.parent.name == 'p' ]

count = 0

for url in all_the_post_urls:
  res = urllib2.urlopen(url)
  post_html = res.read()
  post_soup = BeautifulSoup(post_html)
  dt = helper.parse_date(post_soup)
  post_id = parse_id(url)
  
  directory = helper.FOLDERNAME + '/' + dt.strftime("%Y-%m-%d") + '/'
  if not os.path.exists(directory):
      os.mkdir(directory)
  
  path = directory + post_id + '.html'
  if not os.path.exists(path):
    f = open(path, 'w')
    f.write(post_html)
    f.close()
    count += 1
  else:
    break;
    
print 'Found ' + str(count)
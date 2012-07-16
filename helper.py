import re
import datetime
import time
from bs4 import BeautifulSoup

class Pacific_tzinfo(datetime.tzinfo):
    """Implementation of the Pacific timezone."""
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-8) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)
    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "PST"
        else:
            return "PDT"

def parse_date(post_soup):
  match = post_soup.findAll(text=re.compile("Date: .*"), limit=1)
  full_date_str = match[0]
  just_date_str = re.match("\s?Date:\s?(.*) \w\w\w", full_date_str).group(1)
  date_as_utc = datetime.datetime.strptime(just_date_str, "%Y-%m-%d, %I:%M%p")
  date_aware = date_as_utc.replace(tzinfo=Pacific_tzinfo())
  return date_aware

def parse_id_from_url(url):
  return re.search('\d{10}', url).group(0)
  
  
def parse_title(full_title):
  # near the end of the string for something that's in parens
  # tricky case is if a post has like (blah) (loc) in the title; 
  # make sure we get the rightmost by disallowing internal parens
  loc_m = re.search(r"(\((?P<location>[^)]*)\))?\Z", full_title)
  location = loc_m.group('location')
  full_title = full_title[0:loc_m.start()]

  age_m = re.search(r"(\s\-\s)?(?P<age>\d+)?\s?\Z", full_title)
  age = None
  if age_m.group('age'):
    age = int(age_m.group('age'))
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
  for node in userbody.findAll(text=True):
    if not node.string:
      continue
    elif 'START CLTAGS' in node.string:
      break
    else:
      body += node.string

  post_dict['body'] = body
  return post_dict
  


import re
import datetime

def parse_date(post_soup):
  match = post_soup.findAll(text=re.compile("Date: .*"), limit=1)
  date_str = match[0][7:]
  date = datetime.datetime.strptime(date_str, "%Y-%m-%d, %I:%M%p %Z")
  return date
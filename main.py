import webapp2
from bs4 import BeautifulSoup
import urllib2
import helper
import operator
from google.appengine.ext.webapp import template
from model import MisHTML, Mis
import missearch
import google.appengine.ext.db as db

template.register_template_library('templates.mistags')

PARSER_VERSION = 3

class GetNewHandler(webapp2.RequestHandler):
  def get(self):
    force_fetch = bool(self.request.get('force_fetch'))
    response = urllib2.urlopen('http://sfbay.craigslist.org/sfc/mis/')
    html = response.read()
    soup = BeautifulSoup(html)
    all_the_post_urls = [anchor['href'] for anchor 
      in soup.findAll('a') if anchor.parent.name == 'p' ]
    
    count = 0
    
    for url in all_the_post_urls:
      res = urllib2.urlopen(url)
      post_html = res.read()
      post_soup = BeautifulSoup(post_html)
      dt = helper.parse_date(post_soup)
      post_id = helper.parse_id_from_url(url)
      
      if (not MisHTML.get_by_key_name(post_id)) or force_fetch:
        m_h = MisHTML(html = unicode(post_html, errors='ignore'), posted = dt, key_name = post_id)
        m_h.put()
        count += 1
      else:
        break;
      
    self.response.out.write('Found ' + str(count))

class ParseNewHTMLHandler(webapp2.RequestHandler):
  def get(self):
    count = 0
    for m_h in MisHTML.all().filter('parsed_version <', PARSER_VERSION):
      post_dict = helper.parse_post(m_h.html, m_h.key().name())
      m = Mis(key_name = post_dict['id'],
              html = m_h.html, 
              post_id = post_dict['id'],
              url = post_dict['url'],
              title = post_dict['title'],
              body = post_dict['body'],
              location = post_dict['location'],
              age = post_dict['age'],
              me_gender = post_dict['me_gender'],
              you_gender = post_dict['you_gender'],
              posted = m_h.posted)
      m.put()
      m_h.parsed_version = PARSER_VERSION
      m_h.put()
      count += 1
      
    self.response.out.write('Parsed ' + str(count))

class MainHandler(webapp2.RequestHandler):
  def get(self):
    misses = Mis.all().order('-posted').fetch(50)
    self.response.out.write(template.render('templates/index.html',{'misses':misses}))

class IndexHandler(webapp2.RequestHandler):
  def get(self):
    missearch.indexEverything()
    
class SearchHandler(webapp2.RequestHandler):
  def get(self, query_string):
    post_ids = missearch.missearch(query_string)
    misses = Mis.get_by_key_name(post_ids)
    self.response.out.write(template.render('templates/search.html',{'misses':misses}))
    

class SummarizeHandler(webapp2.RequestHandler):
  def get(self, field):

    def summarize_field(field):
      missed_connections = [db.to_dict(m) for m in Mis.all()]
      values = [p[field] for p in missed_connections]
      valuecounts = dict((i,values.count(i)) for i in set(values) if i)
      return sorted(valuecounts.iteritems(), key=operator.itemgetter(1), reverse=True)

    counts = summarize_field(field)
    vals = {'counts': counts}
    self.response.out.write(template.render('templates/summarize.html',vals))


app = webapp2.WSGIApplication([('/', MainHandler),
                              (r'/summarize/(.*)',SummarizeHandler),
                              ('/getnew', GetNewHandler),
                              ('/indexeverything', IndexHandler),
                              (r'/search/(.*)',SearchHandler), 
                              ('/parsenew', ParseNewHTMLHandler)],
                              debug=True)

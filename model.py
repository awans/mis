import google.appengine.ext.db as db

class MisHTML(db.Model):
  html = db.TextProperty()
  posted = db.DateTimeProperty()
  parsed_version = db.IntegerProperty(default=0)

class Mis(db.Model):
  html = db.TextProperty()
  post_id = db.StringProperty()
  url = db.StringProperty()
  title = db.StringProperty()
  body = db.TextProperty()
  location = db.StringProperty()
  age = db.IntegerProperty()
  me_gender = db.StringProperty()
  you_gender = db.StringProperty()
  posted = db.DateTimeProperty()
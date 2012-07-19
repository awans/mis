from google.appengine.ext.webapp import template

register = template.create_template_register()

def render_mis(mis):
  return { "mis":mis }
  
register.inclusion_tag('mis.html')(render_mis)
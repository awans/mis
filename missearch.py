from google.appengine.api import search
import model
import logging

_INDEX_NAME="misses"

def CreateDocument(mis):
	return search.Document(
	doc_id = mis.post_id,
	  fields=[
  	  search.TextField(name="body", value=(mis.body or "")), 
	    search.TextField(name="title", value=(mis.title or "")),
	    search.TextField(name="location", value=(mis.location or "")),
	    search.NumberField(name="age", value=(mis.age or -1)),
	    search.DateField(name="posted", 
	      value=mis.posted.date()),
	    search.AtomField(name="you_gender",
	      value=(mis.you_gender or "")),
	    search.AtomField(name="me_gender", 
	      value=(mis.me_gender or "")) 
	  ])


def indexEverything():
  index = search.Index(name=_INDEX_NAME)
  
  for mis in model.Mis.all():
    doc = CreateDocument(mis)
    try:
      index.add(doc)
    except search.Error:
      logging.exception("indexing failed for document id: %s"  % mis.post_id)
      
def missearch(query_string):
  """Returns a list of matching post_ids for a given query"""
  try:
    results = search.Index(name=_INDEX_NAME).search(query_string)
    return [doc.doc_id for doc in results]
  except search.Error:
    logging.exception('Search failed')

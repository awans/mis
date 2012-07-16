import pickle
import helper
import operator
import pprint

def summarize_field(field):
  values = [p[field],  for p in missed_connections]
  valuecounts = dict((i,values.count(i)) for i in set(values))
  return sorted(valuecounts.iteritems(), key=operator.itemgetter(1))

f = open(helper.PICKLEJAR, 'r')
missed_connections = pickle.load(f)

missed_connections
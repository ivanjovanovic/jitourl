from google.appengine.ext import db
import hashlib
from model.counter import *
from base64 import urlsafe_b64encode, urlsafe_b64decode

class Mapping(db.Model):
    url = db.StringProperty()
    shortcode = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class MappingService():
    
    counter_name = "cnt_general"
    
    def getUrlForShortcode(self, shortcode):
        mapping = Mapping.gql("WHERE shortcode = :1", shortcode).get()
        if mapping == None:
            return None
            
        return mapping.url
        
    def getShortcodeForUrl(self, url):
        mapping = Mapping.gql("WHERE url = :1", url).get()
        if mapping == None:
            return None

        return mapping.shortcode
        
    def createNewMappingEntry(self, url):
        cnt = self.getCounter()
        cnt.increment()
        shortcode = urlsafe_b64encode("%s" % cnt.count).strip('=')

        hasher = hashlib.md5()
        hasher.update(url)
        key = hasher.hexdigest()
        
        map_entry = Mapping(key_name=key)
        map_entry.url = url
        map_entry.shortcode = shortcode
        map_entry.put()
        
        return shortcode
        
    def getCounter(self):
        cntFact = CounterFactory()
        return cntFact.get_counter(self.counter_name)

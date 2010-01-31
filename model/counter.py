from google.appengine.ext import db

class CounterFactory:
    def get_counter(self, key_name):
        return Counter.get_or_insert(key_name)

class Counter(db.Model):
    count = db.IntegerProperty(default=0)
    
    def increment(self):
        self.count += 1
        self.put()
        
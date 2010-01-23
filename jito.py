import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Mapping(db.Model):
    url = db.StringProperty()
    ji = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class MappingService(Mapping):
    def getUrlForJI(self, ji):
        return
    def getJIForURL(self, url):
        return
    def crateNewJI(self, url):
        return

class RevCanonical():
    def checkUrl():
        return

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        mappings = db.GqlQuery("SELECT * FROM Mapping ORDER BY date DESC LIMIT 10")
        
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'mappings': mappings}))

class CreateCode(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        mapping = Mapping()
        mapping.url = 'Test URL'
        mapping.ji = 'Test JI'
        mapping.put()
        
        self.redirect('/')
        

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/create', CreateCode)],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from model.mapping import *
from urlparse import urlparse

class RedirectToUrl(webapp.RequestHandler):
    def get(self):
        # get url for the shortcode
        
        url = None
        parsed_url = urlparse(self.request.url)
        mappings = MappingService()
        url = mappings.getUrlForShortcode(parsed_url.path.lstrip('/'))
        
        if url == None:
            url = "%s://%s/" % (parsed_url.scheme, parsed_url.netloc)
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.set_status(301)
        self.response.headers['Location'] = url

application = webapp.WSGIApplication([('/.*', RedirectToUrl)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
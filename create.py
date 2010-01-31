from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from model.mapping import *
from urlparse import urlparse

class CreateShortUrl(webapp.RequestHandler):
    def post(self):
        # implement validation on URL
        url_is_valid = self.isUrlValid(self.request.get('url'))
        
        # if invalid url is given then redirect back to homepage with error message
        if url_is_valid == False:
            parsed_url = urlparse(self.request.url)
            url = "%s://%s/" % (parsed_url.scheme, parsed_url.netloc) # change to default domain where we are currently
            self.response.headers['Content-Type'] = 'text/html'
            self.response.set_status(303)
            self.response.headers['Location'] = url
            return
        
        # check if url doesn't exist
        mappings = MappingService()
        shortcode = mappings.getShortcodeForUrl(self.request.get('url'))

        if shortcode == None:
            shortcode = mappings.createNewMappingEntry(self.request.get('url'))
        
        server_parsed_url = urlparse(self.request.url)
        shortUrl = "%s://%s/%s" % (server_parsed_url.scheme, server_parsed_url.netloc, shortcode)
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'shortUrl' : shortUrl }))

    def isUrlValid(self, url):
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ['http', 'https']:
            return False

        if parsed_url.netloc.find('.') == -1:
            return False

        return True


application = webapp.WSGIApplication(
                                     [('/create', CreateShortUrl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
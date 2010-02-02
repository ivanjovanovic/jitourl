import os
import sys
from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from model.mapping import *
from model.revcanonical import *

class CreateShortUrl(webapp.RequestHandler):
    def post(self):
        # implement validation on URL
        user_provided_url = self.request.get('url')
        url_is_valid = self.isUrlValid(user_provided_url)
        
        # if invalid url is given then redirect back to homepage with error message
        if url_is_valid == False:
            parsed_url = urlparse(self.request.url)
            url = "%s://%s/" % (parsed_url.scheme, parsed_url.netloc) # change to default domain where we are currently
            self.response.out.write("Did you really provide URL? Go back here %s and try again." % url)
            return
        
        # check if URL owner provided rev="canonical" link to the existing shortcut
        revc = RevCanonical()
        owner_provided_shorturl = revc.checkUrl(user_provided_url)
        
        if owner_provided_shorturl == None:            
            # check if url already exists in mappings
            mappings = MappingService()
            shortcode = mappings.getShortcodeForUrl(user_provided_url)
            
            # if it doesn't exist, generate new mapping
            if shortcode == None:
                # check if user provided custom alias
                user_provided_shortcode = self.request.get('alias', default_value = None)
                shortcode = mappings.createNewMappingEntry(user_provided_url, user_provided_shortcode)
            
            # build short url
            server_parsed_url = urlparse(self.request.url)
            shortUrl = "%s://%s/%s" % (server_parsed_url.scheme, server_parsed_url.netloc, shortcode)
            
        else:
            shortUrl = owner_provided_shorturl
        
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {'shortUrl' : shortUrl }))

    def isUrlValid(self, url):
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ['http', 'https']:
            return False

        if parsed_url.netloc.find('.') == -1:
            return False

        return True

    def isShortcutValid():
        pass

application = webapp.WSGIApplication(
                                     [('/create', CreateShortUrl)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
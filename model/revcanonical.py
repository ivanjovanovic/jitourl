from urllib import urlopen

class RevCanonical():
    
    revc_api = "http://revcanonical.appspot.com/api?url="
    def checkUrl(self, url):
        try:
            result = urlopen("%s%s" % (self.revc_api,url))
            potentialy_revc = result.readline()
            if potentialy_revc != url:
                return potentialy_revc
            else:
                return None

        except IOError, e:
            return None


from model.revcanonical import *
import unittest

class TestRevCanonical(unittest.TestCase):
    
    test_url = "http://shiflett.org/blog/2009/apr/save-the-internet-with-rev-canonical"
    test_rev = "http://tr.im/revcanonical"
    
    def testExistingRev(self):
        revc = RevCanonical()
        owner_provided = revc.checkUrl(self.test_url)
        
        self.assertEqual(owner_provided, self.test_rev)
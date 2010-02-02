from model.mapping import *
import unittest
import hashlib

class TestMappingService(unittest.TestCase):

    test_url = "http://www.sometesturl.com/?param1=value1&param2=value2"
    test_shortcode = 'test_shortcode'
    
    def setUp(self):
        pass
    
    def tearDown(self):
        mappings = MappingService()
        counter = mappings.getCounter()
        counter.delete()
    
    def testCreatingNewShortcut(self):
        mappings = MappingService()
        shortcode = mappings.createNewMappingEntry(self.test_url)
        
        # it is expected that mapping increment counter before creating new hash from it
        cnt = mappings.getCounter()
        self.assertEqual(1, cnt.count)
        
        # we expect to see entry with the hash of the url in the mappings list
        hasher = hashlib.md5()
        hasher.update(self.test_url)
        map_entry = Mapping.get_by_key_name(hasher.hexdigest())
        
        self.assertEqual(self.test_url, map_entry.url)
        self.assertEqual(shortcode, map_entry.shortcode)

    def testCreatingNewShortcutWithPredefinedShortcode(self):
        mappings = MappingService()
        shortcode = mappings.createNewMappingEntry(self.test_url, self.test_shortcode)

        # it is expected that mapping increment counter doesn't increment when shortcode is provided
        cnt = mappings.getCounter()
        self.assertEqual(0, cnt.count)

        # we expect to see entry with the hash of the url in the mappings list
        hasher = hashlib.md5()
        hasher.update(self.test_url)
        map_entry = Mapping.get_by_key_name(hasher.hexdigest())

        self.assertEqual(self.test_url, map_entry.url)
        self.assertEqual(self.test_shortcode, map_entry.shortcode)
        
    def testGettingURLforShortcode(self):
        mappings = MappingService()
        shortcode = mappings.createNewMappingEntry(self.test_url)
        
        url = mappings.getUrlForShortcode(shortcode)
        self.assertEqual(url, self.test_url)
    
    def testGettingURLforShortcodeNonExistingShortcode(self):
        mappings = MappingService()        
        url = mappings.getUrlForShortcode("shortcode")
        self.assertEqual(url, None)
        
    def testGettingShortcutForURL(self):
        mappings = MappingService()
        shortcode = mappings.createNewMappingEntry(self.test_url)
        
        shortcodeTested = mappings.getShortcodeForUrl(self.test_url)
        self.assertEqual(shortcode, shortcodeTested)
        
    def testGettingShortcodeForUrlNonExistingUrl(self):
        mappings = MappingService()
        shortcode = mappings.getShortcodeForUrl("http://www.someurl.com")
        self.assertEqual(shortcode, None)
    def testGettingCounter(self):
        mappings = MappingService()
        counter = mappings.getCounter()
        
        # test counter type
        self.assertTrue(isinstance(counter, Counter))
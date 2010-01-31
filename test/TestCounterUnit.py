import unittest
from model.counter import *

class TestCounter(unittest.TestCase):
    
    key_name = "cnt_global"
    
    def setUp(self):
        pass
    
    def tearDown(self):
        cntFact = CounterFactory()
        cnt = cntFact.get_counter(self.key_name)
        cnt.delete()
    
    def testCounterInitialState(self):
        cntFact = CounterFactory()
        cnt = cntFact.get_counter(self.key_name)
        self.assertEqual(0, cnt.count)
    
    def testCounterIncrement(self):
        cntFact = CounterFactory()
        cnt = cntFact.get_counter(self.key_name)
        cnt.increment()
        
        cntIncremented = cntFact.get_counter(self.key_name)
        self.assertEqual(1, cntIncremented.count)
        
        #increment again
        cnt.increment()
        
        cntIncremented2 = cntFact.get_counter(self.key_name)
        self.assertEqual(2, cntIncremented2.count)

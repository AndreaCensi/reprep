import unittest
from reprep import Node


class Test(unittest.TestCase):

    def setUp(self):
        self.n1 = Node('n1')
        self.n2 = self.n1.data('n2', None)
        self.n3 = self.n2.data('n3', None)

    def test1(self):
        ''' Testing normal cases of resolve_url '''
        self.assertEqual(self.n2, self.n1.resolve_url('n2'))
        self.assertEqual(self.n3, self.n1.resolve_url('n2/n3'))
        
    def test_not_existent(self):
        ''' Testing that we warn if not existent '''
        self.assertRaises(Node.NotExistent, self.n1.resolve_url, 'x')

    def test_well_formed(self):
        ''' Testing that we can recognize invalid urls '''
        self.assertRaises(Node.InvalidURL, self.n1.resolve_url, '')
        self.assertRaises(Node.InvalidURL, self.n2.resolve_url, '//')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()

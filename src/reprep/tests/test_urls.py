# -*- coding: utf-8 -*-
import unittest
from reprep import Node, NotExistent, InvalidURL


class Test(unittest.TestCase):

    def setUp(self):
        # n1 -- n2 -- n3 -- n4
        #    \_ n3bis
        self.n1 = Node('n1')
        self.n3bis = self.n1.data('n3', None)
        self.n2 = self.n1.data('n2', None)
        self.n3 = self.n2.data('n3', None)
        self.n4 = self.n3.data('n4', None)
        self.all = [self.n1, self.n2, self.n3, self.n4, self.n3bis]

    def test_normal(self):
        ''' Testing normal cases of resolve_url '''
        self.assertEqual(self.n1, self.n2.resolve_url('..'))
        self.assertEqual(self.n1, self.n3.resolve_url('../..'))
        self.assertEqual(self.n1, self.n4.resolve_url('../../..'))
        self.assertEqual(self.n2, self.n4.resolve_url('../../../n2'))
        self.assertEqual(self.n2, self.n1.resolve_url('n2'))
        self.assertEqual(self.n3, self.n1.resolve_url('n2/n3'))

    def test_smart(self):
        ''' Testing smart cases of resolve_url '''
        self.assertEqual(self.n1.resolve_url('n3'), self.n3bis)
        self.assertEqual(self.n2.resolve_url('n3'), self.n3)
        self.assertEqual(self.n3.resolve_url('n3'), self.n3)
        self.assertEqual(self.n2.resolve_url('n1/n3'), self.n3bis)
        self.assertEqual(self.n3.resolve_url('n1/n3'), self.n3bis)
        self.assertEqual(self.n4.resolve_url('n4'), self.n4)
        self.assertEqual(self.n3.resolve_url('n4'), self.n4)
        self.assertEqual(self.n2.resolve_url('n4'), self.n4)
        self.assertEqual(self.n1.resolve_url('n4'), self.n4)
        for n in self.all:
            self.assertEqual(n.resolve_url('n4'), self.n4)

    def test_relative(self):
        for A in self.all:
            for B in self.all:
                if A == B:
                    continue
                url = A.get_relative_url(B)
                self.assertEqual(A.resolve_url_dumb(url), B)

    def test_not_existent(self):
        ''' Testing that we warn if not existent '''
        self.assertRaises(NotExistent, self.n1.resolve_url, 'x')

    def test_not_found(self):
        self.assertRaises(NotExistent, self.n1.resolve_url, '..')

    def test_well_formed(self):
        ''' Testing that we can recognize invalid urls '''
        self.assertRaises(InvalidURL, self.n1.resolve_url, '')
        self.assertRaises(InvalidURL, self.n2.resolve_url, '//')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()

# http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
from .. import logger

class CommonEqualityMixin(object):

    def __eq__(self, other):
        if type(other) is not type(self):
            logger.error('Different types: %s != %s' 
                         % (type(other), type(self)))
            return False
        print id(self), self.__dict__.keys()
        
        mine = dict(**self.__dict__)
        his = dict(**other.__dict__)
        if 'parent' in mine:
            del mine['parent']
        if 'parent' in his:
            del his['parent']
                
        if mine.keys() != his.keys():
            return False
        
        for k in mine:
            if mine[k] != his[k]:
                logger.error('Different value for %r' % k)
                logger.error(' mine: %s' % mine[k].__repr__())
                logger.error('  his: %s' % his[k].__repr__()) 
                return False
        
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

#
#    def assert_equal(self, other):
#        def bail(msg):
#            raise Exception(msg)
#        
#        if type(other) != type(self):
#            msg = 'Different type %s' % type(other)
#            bail(msg)
#            
#        his = other.__dict__
#        mine = self.__dict__
#        missing = []
#        hasmore = []
#        different = {}
#        for x in mine:
#            if not x in other:
#                missing.append(x)
#            else:
#                if not mine
#        for x 
                 

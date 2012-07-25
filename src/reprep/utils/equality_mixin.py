## http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
#
#class CommonEqualityMixin(object):
#
#    def __eq__(self, other):
#        if type(other) is not type(self):
#            return False
#        
#        mine = dict(**self.__dict__)
#        his = dict(**other.__dict__)
#        if 'parent' in mine:
#            del mine['parent']
#        if 'parent' in his:
#            del his['parent']
#                
#        if mine.keys() != his.keys():
#            return False
#        
#        for k in mine:
#            if mine[k] != his[k]:
#                return False
#        
#        return True
#
#    def __ne__(self, other):
#        return not self.__eq__(other)

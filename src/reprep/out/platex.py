
from StringIO import StringIO

class Latex:
    
    @staticmethod
    def document(filename, graphics_path):
        pass
    
        @staticmethod
    def fragment(filename, graphics_path):
        pass
    
    
class LatexContext:
    def __init__(self,):
        self.f = StringIO()
        self.preamble = StringIO()
        self.images = {}
        
    def hspace(self):
        self.f.write('\\hspace\ \n')
        
    def input(self, filename):
        self.f.write('\\input{%s}\n' % filename)
    
    def use_package(self, name, options=None):
        pass
        
class Figure(LatexContext):
    de

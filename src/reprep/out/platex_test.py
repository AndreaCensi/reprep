import unittest
import tempfile
import os
import shutil

from reprep.out.platex import Latex

class Test(unittest.TestCase): 

    def testEmpty(self):
        with tempfile.NamedTemporaryFile(suffix='tex') as tmp:
            filename = tmp.name
            with Latex.document(filename) as doc: #@UnusedVariable
                pass
            self.try_compile(tmp)
            
    def testEmptyFigure(self):
        with tempfile.NamedTemporaryFile(suffix='tex') as tmp:
            filename = tmp.name
            with Latex.document(filename) as doc:
                with doc.figure(caption="") as fig:
                    pass
                
            self.try_compile(tmp)

    def testSubFigure(self):
        with tempfile.NamedTemporaryFile(suffix='tex') as tmp:
            filename = tmp.name
            with Latex.document(filename) as doc:
                with doc.figure(caption="") as fig:
                    with fig.subfigure(caption="fig1") as sub:
                        sub.text('ciao')
                    with fig.subfigure(caption="fig2") as sub:
                        sub.text('hello')
                    
            self.try_compile(tmp)

#    def testGraphics(self):
#        with tempfile.NamedTemporaryFile(suffix='tex') as tmp:
#            filename = tmp.name
#            with Latex.document(filename) as doc:
#                with doc.figure(caption="") as fig:
#                    with fig.subfigure(caption="fig1") as sub:
#                        sub.text('ciao')
#                    with fig.subfigure(caption="fig2") as sub:
#                        sub.text('hello')
#                    
#            self.try_compile(tmp)

    def try_compile(self, tmp):
        filename = tmp.name
        command = "pdflatex --interaction batchmode %s" % filename
        res = os.system(command)
        if res != 0:
            d = 'error.tex'
            shutil.copy(filename, d)
#            with open(filename) as f:
#                with open(d, 'w') as fd:
#                    fd.write(f.read())
#                     
            raise Exception('Could not execute command. Dumped on %s.' % d) 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

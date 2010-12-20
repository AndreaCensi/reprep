import unittest
import tempfile
import os
import shutil

from reprep.out.platex import Latex
from subprocess import Popen
import subprocess
from contextlib import contextmanager

class Test(unittest.TestCase): 

    def setUp(self):
        self.test_directory = tempfile.mkdtemp(prefix='tmp-reprep-tests')
        
    def tearDown(self):
        # # TODO: cleanup, remove dir
        pass
    
    @contextmanager
    def get_random_file(self):
        (fd, filename) = tempfile.mkstemp(suffix='tex', dir=self.test_directory)
        yield filename
        # TODO: cleanup
    
    def testEmpty(self):
        with  self.get_random_file() as filename:
            with Latex.document(filename) as doc: #@UnusedVariable
                pass
            self.try_compile(filename)
            
    def testEmptyFigure(self):
        with self.get_random_file() as  filename:
            with Latex.document(filename) as doc:
                with doc.figure(caption="") as fig: #@UnusedVariable
                    pass
            self.try_compile(filename)

    def testSubFigure(self):
        with self.get_random_file()  as filename:
            with Latex.document(filename) as doc:
                with doc.figure(caption="") as fig:
                    with fig.subfigure(caption="fig1") as sub:
                        sub.text('ciao')
                    with fig.subfigure(caption="fig2") as sub:
                        sub.text('hello')
                    
            self.try_compile(filename)

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

    def try_compile(self, filename):
        filename = os.path.basename(filename)
        command = ["pdflatex", "--interaction", "batchmode", filename]
        val = subprocess.call(command, cwd=self.test_directory,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if val != 0:
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

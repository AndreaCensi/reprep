import tempfile, os, unittest, shutil

class ReprepTest(unittest.TestCase):
    
    def node_serialization_ok(self, node):
        directory = tempfile.mkdtemp(prefix='tmp_reprep')
        filename = os.path.join(directory, 'index.html')
        node.to_html(filename)
        shutil.rmtree(directory)
        

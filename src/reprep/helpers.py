import mimetypes
import tempfile

 
class Attacher:
    def __init__(self, node, id, mime):
        self.node = node
        self.id = id
        self.mime = mime
        if self.mime is not None:
            suffix = mimetypes.guess_extension(self.mime)
            if not suffix:
                raise Exception('Cannot guess extension for MIME "%s".' % mime)
        else:
            suffix = '.bin'
        
        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        
    def __enter__(self):
        return self.temp_file.name
        
    def __exit__(self, type, value, traceback): #@UnusedVariable
        with open(self.temp_file.name) as f:
            data = f.read()
            self.node.data(id=self.id, data=data, mime=self.mime)
        self.temp_file.close()


from matplotlib import pylab

class PylabAttacher:
    def __init__(self, node, id, mime):
        self.node = node
        self.id = id
        self.mime = mime
        if self.mime is not None:
            suffix = mimetypes.guess_extension(self.mime)
            if not suffix:
                raise Exception('Cannot guess extension for MIME "%s".' % mime)
        else:
            suffix = '.bin'
        
        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        
        self.figure = pylab.figure()
        
    def __enter__(self):
        return pylab 
        
    def __exit__(self, type, value, traceback): #@UnusedVariable
        
        pylab.savefig(self.temp_file.name)
        pylab.close()
        
        with open(self.temp_file.name) as f:
            data = f.read()
            self.node.data(id=self.id, data=data, mime=self.mime)
        self.temp_file.close()

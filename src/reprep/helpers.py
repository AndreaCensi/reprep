import mimetypes, tempfile, subprocess

 
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

class PylabAttacher:
    def __init__(self, node, id, mime, **figure_args):
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
        
        import matplotlib
        if matplotlib.get_backend() != 'agg':
            matplotlib.use('agg')
        from matplotlib import pylab
        self.pylab = pylab 
        self.figure = self.pylab.figure(**figure_args)
        
    def __enter__(self):
        return self.pylab 
        
    def __exit__(self, exc_type, exc_value, traceback): #@UnusedVariable
        if exc_type is not None:
            # an error occurred. Close the figure and return false.
            self.pylab.close()
            return False
        
        if not self.figure.axes:
            raise Exception('You did not draw anything in the image.')
 
        self.pylab.savefig(self.temp_file.name, bbox_inches='tight', pad_inches=0.2)
        
        self.pylab.close()
        
        with open(self.temp_file.name) as f:
            data = f.read()
            image_node = self.node.data(id=self.id, data=data, mime=self.mime)
        
        # save a png copy if one is needed
        if not self.temp_file.name.endswith('png'):
            with image_node.data_file('png', 'image/png') as f2:
                subprocess.check_call(['convert', self.temp_file.name, f2])
            
        self.temp_file.close()
        
def data_rgb_imp(parent, id, rgb):
    from reprep.graphics.conversions import Image_from_array

    pil_image = Image_from_array(rgb)
        
    with parent.data_file(id, 'image/png') as f:
        pil_image.save(f)
        
    return parent[id]

        

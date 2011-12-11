from . import RepRepDefaults, MIME_PNG, contract, Node
import mimetypes
import tempfile
import subprocess 
 
class Attacher:
    
    @contract(node=Node, nid='valid_id', mime='None|str', caption='None|str')
    def __init__(self, node, nid, mime, caption):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption
        if self.mime is not None:
            suffix = mimetypes.guess_extension(self.mime)
            if not suffix:
                raise Exception('Cannot guess extension for MIME %r.' % mime)
        else:
            suffix = '.bin'
        
        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        
    def __enter__(self):
        return self.temp_file.name
        
    def __exit__(self, _a, _b, _c): 
        with open(self.temp_file.name) as f:
            data = f.read()
            self.node.data(nid=self.nid, data=data,
                           mime=self.mime,
                           caption=self.caption)
        self.temp_file.close()

class PylabAttacher:
    
    @contract(node=Node, nid='valid_id', mime='None|str', caption='None|str')
    def __init__(self, node, nid, mime, caption, **figure_args):
        self.node = node
        self.nid = nid
        self.mime = mime
        self.caption = caption
        
        if self.mime is None:
            self.mime = RepRepDefaults.default_image_format 
            
        suffix = mimetypes.guess_extension(self.mime)
        if not suffix:
            raise Exception('Cannot guess extension for MIME %r.' % mime)
        
        self.temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        
        from . import reprep_pylab_instance
        self.pylab = reprep_pylab_instance 
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
 
        self.pylab.savefig(self.temp_file.name,
                           bbox_inches='tight',
                           pad_inches=0.01) # TODO: make parameters
        
        
        with open(self.temp_file.name) as f:
            data = f.read()
        
        image_node = self.node.data(nid=self.nid, data=data,
                                    mime=self.mime, caption=self.caption)
        
        # save a png copy if one is needed
        if not self.temp_file.name.endswith('png'):
            # TODO: use savefig() instead of "convert"
            # self.pylab.savefig(self.temp_file.name, bbox_inches='tight', pad_inches=0.2)
        
            with image_node.data_file('png', mime=MIME_PNG,
                                      caption=self.caption) as f2:
                density = 300
                subprocess.check_call(['convert', '-density', '%s' % density,
                                        self.temp_file.name, f2])
#        
            from . import Figure
            if isinstance(self.node, Figure):
                self.node.sub(image_node)
                
        self.pylab.close()

        self.temp_file.close()
        
@contract(parent=Node, nid='valid_id', rgb='array[HxWx(3|4)]', caption='None|str')
def data_rgb_imp(parent, nid, rgb, caption=None):
    from reprep.graphics.conversions import Image_from_array

    pil_image = Image_from_array(rgb)
        
    with parent.data_file(nid=nid, mime=MIME_PNG, caption=caption) as f:
        pil_image.save(f)
        
    return parent[nid]

        

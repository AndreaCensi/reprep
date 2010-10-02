
class ReportInterface: 
 
    def data(self, id, data, mime=None, desc=None):
        ''' Attaches a data child to this node. 
        
            "data" is assumed to be a raw python structure. 
            Or, if data is a string representing a file, 
            pass a proper mime type (mime='image/png'). 
            
            Returns a reference to the node being created.
        '''
        if not isinstance(id, str):
            raise ValueError('The ID must be a string, not a %s' % \
                             id.__class__.__name__) 
        from reprep import DataNode
        n = DataNode(id=id, data=data, mime=mime)
        self.add_child(n) 
        return n
    
    def data_file(self, id, mime):
        ''' Support for attaching data from a file. Note: this method is 
        supposed to be used in conjunction with the "with" construct. 
        
        For example, the following is the concise way to attach a pdf
        plot to a node.::
        
            with report.data_file('my_plot', 'application/pdf') as f:
                pylab.figure()
                pylab.plot(x,y)
                pylab.title('my x-y plot')
                pylab.savefig(f)
        
        Omit any file extension from 'id', ("my_plot" and not "my_plot.pdf"), 
        we will take care of it for you.
        
        This is a more complicated example, where we attach two versions
        of the same image, in different formats::
         
            for format in ['application/pdf', 'image/png']:
                with report.data_file('plot', format) as f:
                    pylab.figure()
                    pylab.plot(x,y)
                    pylab.savefig(f)
                    pylab.close()
                    
        Note that if you are mainly using pylab plots, there is the function
        :py:func:`.data_pylab` which offers a shortcut with less ceremony.
        '''
        from helpers import Attacher
        import mimetypes
        
        if not mimetypes.guess_extension(mime):
            raise ValueError('Cannot guess extension for MIME "%s".' % mime)
        
        return Attacher(self, id, mime)
 
    def data_pylab(self, id, mime='image/png', **figure_args): 
        ''' Easy support for creating a node consisting of a pylab plot.
        Note: this method is supposed to be used in conjunction with 
        the "with" construct. 
        
        For example, the following is the concise way to attach a plot: ::
        
            with report.data_pylab('my_plot') as pylab:
                pylab.plot(x,y)
                pylab.title('my x-y plot')

        Basically, data_pylab allows you to save some lines of code 
        more than with :py:func:`.data_file`.
        
        You can pass **figure_args to pylab.figure().
        
         '''
        import mimetypes
        from reprep.helpers import PylabAttacher

        
        if not mimetypes.guess_extension(mime):
            raise ValueError('Cannot guess extension for MIME "%s".' % mime)
        
        return PylabAttacher(self, id, mime, **figure_args)

    def figure(self, id=None, sub=[], **kwargs):
        ''' Attaches a figure to this node. '''
        from reprep import Figure
        f = Figure(id, **kwargs)
        self.add_child(f)
        
        for resource in sub:
            f.sub(resource)
 
        return f
 
    def table(self, id, data, col_desc=None):
        ''' Attaches a table to this node. 
            
            data must be either a list of lists, or a 1D numpy array
        
        
        '''
        from reprep import Table
        t = Table(id, data, col_desc)
        self.add_child(t) 
        return t
        

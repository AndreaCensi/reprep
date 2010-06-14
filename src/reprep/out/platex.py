
from StringIO import StringIO
import mimetypes
import os


class Latex:
    
    @staticmethod
    def document(filename, graphics_path=".", document_class="article",
                 class_options=""):
        class BodyWrap:
            def __init__(self, filename, document):
                self.document = document
                self.filename = filename
            def __enter__(self):
                return self.document
            def __exit__(self, type, value, traceback): #@UnusedVariable
                with open(self.filename, 'w') as f:
                    self.document.dump_stream(f)
                   
        document = LatexDocument(graphics_path=graphics_path,
                                 document_class=document_class,
                                 class_options=class_options)
        return BodyWrap(filename, document)
   
    
    @staticmethod
    def fragment(filename, graphics_path):
        class Attacher:
            def __init__(self, filename, graphics_path):
                self.context = LatexContext(graphics_path=graphics_path)
                self.filename = filename
                self.environment = LatexEnvironment(self.context)
            def __enter__(self):
                return self.environment
            def __exit__(self, type, value, traceback): #@UnusedVariable
                with open(self.filename, 'w') as f:
                    f.write(self.context.f.getvalue())
        return Attacher(filename, graphics_path)
    
    
class LatexContext:
    def __init__(self, graphics_path="."):
        self.f = StringIO()
        self.preamble = StringIO()
        self.graphics_path = graphics_path
        self.parent = None
        self.count = 0
        
    def generate_file_id(self):
        if self.parent:
            return self.parent.generate_file_id()
        f = "file%s" % self.count
        self.count += 1 
        return f 
    
    def child(self):
        ''' Generates a child context; sharing some data '''
        c = LatexContext(self.graphics_path)
        c.parent = self
        return c


class LatexEnvironment:
    def __init__(self, context):
        self.context = context
                
    def hfill(self):
        self.context.f.write('\\hfill\ \n')
    
    def parbreak(self):
        self.context.f.write('\n\n')
        
    def pagebreak(self):
        self.context.f.write('\\pagebreak\ \n')

    def rule(self, width, height, color='gray'):
        self.context.f.write('{\\color{%s}\\rule{%s}{%s}}\n' % \
                             (color, width, height))
    
    def text(self, t):
        self.context.f.write(latexify(t))
        
    def table(self, data, row_desc, col_desc, alignment=None, escape=True):
        pass
        
    def tex(self, tex):
        self.context.f.write(tex)
        
    def input(self, filename):
        self.context.f.write('\\input{%s}\n' % filename)
    
    def use_package(self, name, options=""):
        self.context.preamble.write('\\usepackage[%s]{%s}\n' % (options, name))
        
    def figure(self, caption=None, label=None, placement="t"):
        figure = Figure(caption=caption, label=label, placement=placement,
                        context=self.context.child())
        return LatexEnvironment.GenericWrap(figure, self.context)
    
    def graphics_data(self, data, mime, width="3cm", id=None):
        suffix = mimetypes.guess_extension(mime)
        if id is None:
            id = self.context.generate_file_id()
        filename = os.path.join(self.context.graphics_path, id + suffix)
        with open(filename, 'w') as f:
            f.write(data)
        self.context.f.write('\\includegraphics[width=%s]{%s}\n' % (width, id))
        
    class GenericWrap:
        def __init__(self, figure, main_context):
            self.figure = figure
            self.main_context = main_context
        def __enter__(self):
            return self.figure
        def __exit__(self, type, value, traceback): #@UnusedVariable
            self.figure.dump(main_context=self.main_context)
    
    
class LatexDocument(LatexEnvironment):
    def __init__(self, document_class, class_options, graphics_path="."):
        self.context = LatexContext(graphics_path)
        self.document_class = document_class
        self.class_options = class_options
        
    def dump_stream(self, file):
        file.write('\\documentclass[%s]{%s}\n' % (self.class_options,
                                                  self.document_class))
        file.write('\\usepackage{graphicx}\n')
        file.write('\\usepackage{xcolor}\n')
        file.write('\\usepackage{subfig}\n') 
        file.write('\\graphicspath{{%s}}\n' % self.context.graphics_path)
        file.write(self.context.preamble.getvalue())
        file.write('\\begin{document}\n')
        file.write(self.context.f.getvalue())
        file.write('\\end{document}\n')

class Figure(LatexEnvironment):
    def __init__(self, caption, label, placement, context):
        self.caption = caption
        self.label = label
        self.context = context
        self.placement = placement
    
    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    def subfigure(self, caption="", label=None):
        figure = SubFigure(caption=caption, label=label,
                           context=self.context.child())
        return LatexEnvironment.GenericWrap(figure, self.context)
    
    def dump(self, main_context):
        # writes everything, and caption delayed
        main_context.preamble.write(self.context.preamble.getvalue())
        main_context.f.write('\\begin{figure}[%s]\n' % self.placement)
        main_context.f.write(self.context.f.getvalue())
        if self.label:
            label = '\\label{%s}' % self.label
        else:
            label = "" 
        main_context.f.write('\\caption{%s%s}\n' % (label, self.caption))
        main_context.f.write('\\end{figure}\n')
        

class StructureError(Exception):
    pass

class SubFigure(LatexEnvironment):
    def __init__(self, caption, label, context):
        self.caption = caption
        self.label = label
        self.context = context
    
    def figure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    def subfigure(self, *args, **kwargs):
        raise StructureError('Cannot nest figures; use sub().')
    
    def dump(self, main_context):
        body = self.context.f.getvalue()
        if self.label:
            label = "\\label{%s}" % self.label
        else:
            label = ""
        caption = self.caption
        main_context.preamble.write('\\usepackage{subfig}\n')
        
        main_context.f.write('\\subfloat[%s%s]{%s}\n' % (label, caption, body))

        


def latexify(s):
    # XXX TO WRITE and use
    return str(s).replace('_', '\\_')

        
    

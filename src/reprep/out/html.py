import os
import mimetypes
import sys

class html_context:
    def __init__(self, file, rel_resources_dir, resources_dir):
        self.file = file
        self.rel_resources_dir = rel_resources_dir
        self.resources_dir = resources_dir

def htmlfy(s):
    # XXX to write
    return str(s)


def get_complete_id(node):
    if not node.parent:
        return node.id
    else:
        return get_complete_id(node.parent) + ":" + node.id

def get_node_filename(node, context):
    ''' Returns a tuple (relative_from_file, absolute) '''
    suffix = mimetypes.guess_extension(node.mime)
    if suffix is None:
        suffix = '.pickle'
    id = get_complete_id(node)
    id = id.replace('/', '_')
    id = id.replace('.', '_')
    relative = os.path.join(context.rel_resources_dir, id + suffix)
    absolute = os.path.join(context.resources_dir, id + suffix)
    return relative, absolute
    

def node_to_html_document(node, filename):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    rel_resources_dir = basename + '_resources'
    resources_dir = os.path.join(dirname, rel_resources_dir) 
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    with open(filename, 'w') as file:
        file.write('''
<html>
<head>
    <!--<link rel="stylesheet" href="report.css" type="text/css" />-->
    <style type='text/css'>
    
img { width: 120px; border: solid 1px black;}
h { font-family: monospace; font-size: 120%%; color: black; font-weight: bold;  display: block;}

sssection { border: solid 2px gray; display: block; clear: both; padding: 1em; margin: 1em;}

.report-node { display: block; border: solid 2px gray; padding: 1em; margin: 1em}
.report-figure { display: block; border: solid 2px green; padding: 1em; margin: 1em}
.report-figure-caption { display: block; clear: both; border: solid 1px blue;}
.report-subfigure {  padding: 1em; padding-bottom: 0; margin: 1em; border: solid 1px red; display: block;}
.report-subfigure-caption { clear: both; display: block; font-weight: bold; text-align: center; border: solid 1px blue;}

.node-class { margin:1em; float: right; font-family: monospace; color: blue;}
.node-id {margin:1em;  float: right; font-family: monospace; font-weight: bold; color: green;}
.datanode { font-family: monospace; font-weight: bold; }
.datanode-children { margin-left: 1em; }
    </style>
    <title> %s </title>
    
</head>
<body>
''' % str(node.id))
        
        context = html_context(file,
                    resources_dir=resources_dir,
                    rel_resources_dir=rel_resources_dir)
        node_to_html(node, context)
        
        file.write("\n</body></html>")
 

def children_to_html(node, context):
    for child in node.children:
        node_to_html(child, context)
    
def node_to_html(node, context):
    from reprep import Figure, Table, Node, DataNode

    functions = {
        DataNode: datanode_to_html,
        Table: table_to_html,
        Figure: figure_to_html,
        Node: simple_node_to_html
    }
    t = node.__class__
    if not t in functions:
        raise ValueError('Could not find type of %s (%s) in %s.' % (node, t, functions.keys()))
    functions[t](node, context)
    
def table_to_html(figure, context):
    pass

def figure_to_html(node, context):
    complete_id = get_complete_id(node)
    file = context.file
    file.write('''<div style="clear:left" class='report-figure %s' id='%s'>
    ''' % (None, complete_id))  

    file.write('''<span class='node-id'>%s</span>''' % node.id)  
    file.write('<h>%s</h>' % complete_id) 
  
    if node.shape is None:
        node.shape = (1, len(node.subfigures))
        
    nrows, ncols = node.shape  
  
    for i, sub in enumerate(node.subfigures):
        col = i % ncols
        last_col = col == ncols - 1
        first_col = col == 0
        
        style = "float:left;"
        if first_col:
            style += "clear:left"
    
        file.write('<div style="%s" class="report-subfigure"> ' % style)
      
        try:
            actual_resource = node.resolve_url(sub.image)
        except:
            print "Cannot find sub.image url %s" % sub.image.__repr__()
            node.parent.print_tree()
            raise
          
        image_filename, absolute = get_node_filename(actual_resource, context)
        
        file.write('<img src="%s" />' % image_filename)

        file.write('<p class="report-subfigure-caption">%s</p>' % \
                 htmlfy(sub.caption))
        file.write('</div> ')


        if last_col:
            file.write('\n\n')
  
    file.write('<p class="report-figure-caption">%s</p>' % \
             htmlfy(node.caption))
    
    children_to_html(node, context)

    file.write('''</div>''')  


def datanode_to_html(node, context):
    ''' Writes the data on the file '''
    relative, filename = get_node_filename(node, context) #@UnusedVariable
    if node.mime == 'python':
        #print "Ignoring %s" % filename
        pass
    else:
        if not isinstance(node.raw_data, str):
            sys.stderr.write("Ignoring %s because raw_data is %s\n" % \
                (filename, node.raw_data.__clasS__))
        else:
            # print "Writing on %s" % filename
            with open(filename, 'w') as f:
                f.write(node.raw_data)
                
    inline = ""
    
    if node.mime == 'python':
        s = str(node.raw_data)
        if len(s) < 128:
            inline = "<code>%s</code>" % s # TODO: escape
            
    context.file.write('<p class="datanode">Resource: <a href="%s">%s</a> %s</p>\n' % \
                       (relative, node.id, inline))

    context.file.write('<div class="datanode-children">\n')
    children_to_html(node, context)
    context.file.write('</div>\n')


def simple_node_to_html(node, context):
    complete_id = get_complete_id(node)
    
    file = context.file
    
    file.write('''
    <div class='report-node' id="%s">
    ''' % complete_id)
    
    file.write(''' 
    <span class='node-id'>%s </span>
    ''' % (node.id))
    
    file.write('<h>%s</h>' % complete_id) 
    
    file.write('<section> \n')
    
    children_to_html(node, context)
    
    file.write('</section> \n')
    file.write('</div> \n')


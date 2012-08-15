from . import logger
from .. import MIME_PLAIN, MIME_RST, MIME_PYTHON, Node
from pkg_resources import (
    resource_filename) #@UnresolvedImport  Eclipse fails here
from string import Template
import cPickle
import datetime
import mimetypes
import os
import shutil
import sys
from types import NoneType

header = """
<html>
<head>  
    <script type="text/javascript" 
        src="${resources}/static/jquery/jquery.js"></script>
    
    <!-- Use imagezoom plugin --> 
    <script type="text/javascript" 
        src="${resources}/static/jquery/jquery.imageZoom.js"></script>
    <link rel="stylesheet" 
          href="${resources}/static/jquery/jquery.imageZoom.css"/>
    <script type="text/javascript"> 
        $$(document).ready( function () {
            $$('.zoomable').imageZoom();
        });       
    </script>
    
    <style type="text/css">
    /* Extra CSS passed by user. */
        ${extra_css}
    </style>

    <link rel="stylesheet" 
          href="${resources}/static/reprep/default_style.css"/>

    <title> ${title} </title>
<body>

<p id="reprep-head"> 
    Report created on ${date}
    by <a href="http://purl.org/censi/2010/RepRep">RepRep</a>.
    Show:
    <input type="submit" name="datanode_toggle" 
           value="data nodes" id="datanode_toggle" /> 
</p>


<script type="text/javascript">
 $$(document).ready(function() {
   $$('.datanode').hide();
   $$('#datanode_toggle').click(function(){
     $$('.datanode').toggle();
   });
 });
</script>


"""

footer = """
 

</body>
</html>
"""


class html_context:
    def __init__(self, file, #@ReservedAssignment
                 rel_resources_dir, resources_dir, write_pickle):
        self.file = file
        self.rel_resources_dir = rel_resources_dir
        self.resources_dir = resources_dir
        self.write_pickle = write_pickle


def htmlfy(s):
    # XXX to write
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    def html_escape(text):
        """Produce entities within text."""
        return "".join(html_escape_table.get(c, c) for c in text)

    return html_escape(str(s))


def get_complete_id(node, separator='-'):
    if not node.parent:
        return node.nid if node.nid else 'anonymous'
    else:
        return get_complete_id(node.parent) + separator + node.nid


def get_node_filename(node, context):
    ''' Returns a tuple (relative_from_file, absolute) '''
    suffix = mimetypes.guess_extension(node.mime)
    if suffix is None:
        suffix = '.pickle'
    nid = get_complete_id(node)
    nid = nid.replace('/', '_')
    nid = nid.replace('.', '_')
    nid = nid.replace(' ', '_')
    if True:
        # LaTeX has plenty of problems with '_' in the name
        nid = nid.replace('_', '-')

    f = normalize(nid + suffix)

    relative = os.path.join(context.rel_resources_dir, f)
    absolute = os.path.join(context.resources_dir, f)

    return relative, absolute


def normalize(f):
    # convert '-png.png' to '.png'
    base, ext = os.path.splitext(f)
    if len(ext) == 4:
        w = ext[1:]
        if base.endswith(w):
            base = base[:-4]
    return base + ext


def node_to_html_document(node, filename,
                          resources_dir=None,
                          extra_css=None,
                          write_pickle=False):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)

    if resources_dir is None:
        resources_dir = os.path.join(dirname, basename + '_resources')

    rel_resources_dir = os.path.relpath(resources_dir, dirname)

    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)

    # look for static data
    static = resource_filename("reprep", "static")

    if not os.path.exists(static):
        # XXX:
        logger.warn('Warning: resource dir %s not found' % static)
    else:
        dst = os.path.join(resources_dir, 'static')
        if not os.path.exists(dst):
            # XXX: does not work if updated
            shutil.copytree(static, dst)

    with open(filename, 'w') as f:
        mapping = {'resources': rel_resources_dir,
                   'title': str(node.nid),
                   'extra_css': extra_css if extra_css else "",
                   'date': isodate_with_secs()}

        f.write(Template(header).substitute(mapping))

        context = html_context(f,
                    resources_dir=resources_dir,
                    rel_resources_dir=rel_resources_dir,
                    write_pickle=write_pickle)
        node_to_html(node, context)

        f.write(Template(footer).substitute(mapping))


def isodate_with_secs():
    """ E.g., '2011-10-06-22:54:33' """
    now = datetime.datetime.now()
    date = now.isoformat('-')[:19]
    return date


def children_to_html(node, context):
    #from reprep import Figure, Table
    # First figure and tables
    #priority = (Table, Figure, Node)
    #priority = (Table, Figure)
    priority = (NoneType,)

    first = [x for x in node.children if isinstance(x, priority)]
    second = [x for x in node.children if not x in first]

    for child in first:
        node_to_html(child, context)

    if second:
        f = context.file
        f.write('<div class="report-nongui-nodes">\n')
        for child in second:
            node_to_html(child, context)
        f.write('</div>\n')


def node_to_html(node, context):
    from reprep import Figure, Table, DataNode

    functions = {
        DataNode: datanode_to_html,
        Table: table_to_html,
        Figure: figure_to_html,
        Node: simple_node_to_html
    }
    t = node.__class__
    if not t in functions:
        msg = ('Could not find type of %s (%s) in %s.' %
               (node, t, functions.keys()))
        raise ValueError(msg)
    functions[t](node, context)


def table_to_html(table, context):
    f = context.file

    f.write('<table class="report-table">\n')

    caption = table.caption if table.caption else table.nid

    f.write('<caption>%s</caption>\n' % caption)

    f.write('<tbody>\n')

    has_row_labels = filter(None, table.rows)

    if filter(None, table.cols): # at least one not None
        f.write('<tr>\n')
        if has_row_labels:
            f.write('<th></th>')
        for field in table.cols:
            if field is not None:
                f.write('\t<th>%s</th>\n' % field)
            else:
                f.write('\t<th></th>\n')
        f.write('</tr>\n')

    for i, row in enumerate(table.data):
        html_class = {0: 'even', 1: 'odd'}[i % 2]
        f.write('<tr class="%s">\n' % html_class)

        if table.rows[i] is not None:
            f.write('<th>%s</th>\n' % table.rows[i]) # FIXME html escaping
        else:
            if has_row_labels:
                f.write('<th></th>\n')

        #for field in row.dtype.names:
        #  value = row[field]
        for value in row:
            rep = str(value)
            f.write('\t<td>%s</td>\n' % rep)
        f.write('</tr>\n')
    f.write('</tbody>\n')
    f.write('</table>\n')


def figure_to_html(node, context):
    complete_id = get_complete_id(node)
    file = context.file  #@ReservedAssignment # XXX
    file.write('''<div style="clear:left" class='report-figure %s' id='%s'>
    ''' % (None, complete_id))

    #file.write('''<span class='node-id'>%s</span>''' % node.nid)
    if not 'figure' in node.nid.lower():
        # Do not write if name is autogenerated  
        file.write('<h>%s</h>' % node.nid)

    if node.cols is None:
        ncols = len(node.subfigures)
    else:
        ncols = node.cols

    for i, sub in enumerate(node.subfigures):
        col = i % ncols
        last_col = col == ncols - 1

        style = "float:left;"
#        first_col = col == 0
#        if first_col:
#            style += "clear:left;"

        width = "%d%%" % (95.0 / max(ncols, 2))
        style += 'width:%s' % width

        file.write('<div style="%s" class="report-subfigure"> ' % style)

        try:
            actual_resource = node.resolve_url(sub.web_image)
        except:
            logger.error("Cannot find sub.web_image url %r" % sub.web_image)
            node.parent.print_tree() # XXX
            raise

        image_filename, _ = get_node_filename(actual_resource, context)

        file.write(
            Template('''
                <a href="${src}" class="zoomable">
                    <img style="width:95%" src="${src}"/>
                </a>    
            ''').substitute(src=image_filename)
        )

        file.write('<p class="report-subfigure-caption">%s</p>' %
                 htmlfy(sub.caption))
        file.write('</div> ')

        if last_col:
            file.write('\n\n')

    caption = node.caption if node.caption else ""

    file.write('<p class="report-figure-caption">%s</p>' %
             htmlfy(caption))

    children_to_html(node, context)

    file.write('''</div>''')


def rst2htmlfragment(text):
    from docutils.core import publish_string #@UnresolvedImport

    html = publish_string(
           source=text,
           writer_name='html')
    html = html[html.find('<body>') + 6:html.find('</body>')].strip()
    return html


def text2html(text, mime):
    ''' Converts rst to HTML element. '''

    if mime == MIME_PLAIN:
        # FIXME: add escaping here
        return ('<pre class="report-text report-text-plain">%s</pre>' %
                 htmlfy(text))
    elif mime == MIME_RST:
        return rst2htmlfragment(text)
    else:
        assert('Unknown mime %r for text.' % mime)


def datanode_to_html(node, context):
    ''' Writes the data on the file '''
    relative, filename = get_node_filename(node, context) #@UnusedVariable

    text_mimes = [MIME_PLAIN, MIME_RST]

    if node.mime in text_mimes:
        content = text2html(node.raw_data, node.mime)
        
        if node.nid == 'caption':
            context.file.write("""
<div class="textnode report-text-node"> 

    <span class="textid report-text-node-id"></span> 
   
   <div class="report-text-node-content">
     {content}
   </div>
     
</div>  
""".format(content=content))
            
        else:
            context.file.write("""
<div class="textnode report-text-node"> 

    <span class="textid report-text-node-id"> {id} </span> 
   
   <div class="report-text-node-content">
     {content}
   </div>
     
</div>  
""".format(id=node.nid, content=content))

    else:
        if node.mime == MIME_PYTHON:
            #print "Ignoring %s" % filename
            if context.write_pickle:
                with open(filename, 'wb') as f:
                    cPickle.dump(node.raw_data, f)
            # TODO: add other representations for numpy array
        else:
            if not isinstance(node.raw_data, str):
                sys.stderr.write("Ignoring %s because raw_data is %s\n" % 
                    (filename, node.raw_data.__class__))
            else:
                # print "Writing on %s" % filename
                with open(filename, 'w') as f:
                    f.write(node.raw_data)

        inline = ""

        if node.mime == MIME_PYTHON:
            s = str(node.raw_data)
            if len(s) < 128:
                inline = "<code>%s</code>" % s # TODO: escape
            else:
                inline = s[:125] + '...'
        else:
            inline = (node.mime)

        if context.write_pickle:
            name = '<a href="%s">%s</a>: ' % (relative, node.nid)
        else:
            name = '%s:' % node.nid
            
        s = ('<p class="datanode">%s %s</p>\n' % 
                           (name, inline))
        context.file.write(s)

    if node.children:
        context.file.write('<div class="datanode-children">\n')
        children_to_html(node, context)
        context.file.write('</div>\n')


def simple_node_to_html(node, context):
    complete_id = get_complete_id(node)

    f = context.file

    f.write('''
    <div class='report-node' id="%s">
    ''' % complete_id)

    #file.write(''' 
    #<span class='node-id'>%s </span>
    #''' % (node.nid))

    f.write('<h>%s</h>' % node.nid)

    f.write('<section> \n')

    children_to_html(node, context)

    f.write('</section> \n')
    f.write('</div> \n')


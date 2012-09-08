from .. import Report, StoreResults, logger, contract
from contracts import describe_type
from reprep.utils import frozendict2, natsorted
import os
import time


__all__ = ['ReportManager']


class ReportManager:
    
    def __init__(self, outdir):
        self.outdir = outdir
        self.allreports = StoreResults()
        self.allreports_filename = StoreResults()
         
    def add(self, report, report_type, **kwargs):
        from compmake import Promise
        if not isinstance(report, Promise):
            msg = ('ReportManager is mean to be given Promise objects, '
                   'which are the output of comp(). Obtained: %s' 
                   % describe_type(report))
            raise ValueError(msg)
        
        key = frozendict2(report=report_type, **kwargs)
        
        if key in self.allreports:
            msg = 'Already added report for %s' % key
            raise ValueError(msg)

        self.allreports[key] = report

        dirname = os.path.join(self.outdir, report_type)
        basename = "_".join(map(str, kwargs.values()))
        filename = os.path.join(dirname, basename) 
        self.allreports_filename[key] = filename + '.html'
        
    def create_index_job(self):
        from compmake import comp, comp_stage_job_id
        index_filename = os.path.join(self.outdir, 'report_index.html')
        
        for key in self.allreports:
            job_report = self.allreports[key]
            filename = self.allreports_filename[key] 

            write_job_id = comp_stage_job_id(job_report, 'write')
            
            comp(write_report_and_update,
                 job_report, filename, self.allreports_filename, index_filename,
                 write_pickle=False,
                 job_id=write_job_id)
            
def write_report_and_update(report, report_basename, all_reports, index_filename,
                            write_pickle=False):
    html = write_report(report, report_basename, write_pickle=write_pickle)
    index_reports(reports=all_reports, index=index_filename, update=html)

@contract(report=Report, report_basename='str')
def write_report(report, report_basename, write_pickle=False): 
    from conf_tools.utils import friendly_path
    html = report_basename + '.html'
    logger.info('Writing to %r.' % friendly_path(html))
    rd = os.path.join(os.path.dirname(report_basename), 'images')
    report.to_html(html, write_pickle=write_pickle, resources_dir=rd)
    # TODO: save hdf format
    return html

@contract(reports=StoreResults, index=str)
def index_reports(reports, index, update=None): #@UnusedVariable
    """
        Writes an index for the reports to the file given. 
        The special key "report" gives the report type.
        
        reports[dict(report=...,param1=..., param2=...) ] => filename
    """
    #print('Updating because of new report %s' % update)
    from compmake.utils import duration_human
    import numpy as np
    
    dirname = os.path.dirname(index)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    logger.info('Writing on %s' % index)
    
    f = open(index, 'w')
    
    f.write("""
        <html>
        <head>
        <style type="text/css">
        span.when { float: right; }
        li { clear: both; }
        a.self { color: black; text-decoration: none; }
        </style>
        </head>
        <body>
    """)
    
    mtime = lambda x: os.path.getmtime(x)
    existing = filter(lambda x: os.path.exists(x[1]), reports.items())

 
    # create order statistics
    alltimes = np.array([mtime(b) for _, b in existing]) 
    
    def order(filename):
        """ returns between 0 and 1 the order statistics """
        assert os.path.exists(filename)
        histime = mtime(filename)
        compare = (alltimes < histime) 
        return np.mean(compare * 1.0)
        
    def style_order(order):
        if order > 0.95:
            return "color: green;"
        if order > 0.9:
            return "color: orange;"        
        if order < 0.5:
            return "color: gray;"
        return ""     
        
    @contract(k=dict, filename=str)
    def write_li(k, filename, element='li'):
        desc = ",  ".join('%s = %s' % (a, b) for a, b in k.items())
        href = os.path.relpath(filename, os.path.dirname(index))
        if os.path.exists(filename):
            when = duration_human(time.time() - mtime(filename))
            span_when = '<span class="when">%s ago</span>' % when
            style = style_order(order(filename))
            a = '<a href="%s">%s</a>' % (href, desc)
        else:
            style = ""
            span_when = '<span class="when">missing</span>'
            a = '<a href="%s">%s</a>' % (href, desc)
        f.write('<%s style="%s">%s %s</%s>' % (element, style, a, span_when,
                                               element))

        
    # write the first 10
    existing.sort(key=lambda x: (-mtime(x[1])))
    nlast = min(len(existing), 10)
    last = existing[:nlast]
    f.write('<h2 id="last">Last %d reports</h2>\n' % (nlast))

    f.write('<ul>')
    for i in range(nlast):
        write_li(*last[i])
    f.write('</ul>')

    if False:
        for report_type, r in reports.groups_by_field_value('report'):
            f.write('<h2 id="%s">%s</h2>\n' % (report_type, report_type))
            f.write('<ul>')
            r = reports.select(report=report_type)
            items = list(r.items()) 
            items.sort(key=lambda x: str(x[0])) # XXX use natsort   
            for k, filename in items:
                write_li(k, filename)
    
            f.write('</ul>')
    
    f.write('<h2>All reports</h2>\n')

    sections = make_sections(reports)
    
    def write_sections(sections, parents):
        assert 'type' in sections
        assert sections['type'] == 'division'
        field = sections['field']
        division = sections['division']

        f.write('<ul>')
        sorted_values = natsorted(division.keys())
        for value in sorted_values:
            parents.append(value)
            html_id = "-".join(map(str, parents))            
            bottom = division[value]
            if bottom['type'] == 'sample':
                d = {field: value}
                if not bottom['key']:
                    write_li(k=d, filename=bottom['value'], element='li')
                else:
                    f.write('<li> <p id="%s"><a class="self" href="#%s">%s = %s</a></p>\n' 
                            % (html_id, html_id, field, value))
                    f.write('<ul>')
                    write_li(k=bottom['key'], filename=bottom['value'], element='li')
                    f.write('</ul>')
                    f.write('</li>')
            else:
                f.write('<li> <p id="%s"><a class="self" href="#%s">%s = %s</a></p>\n' 
                        % (html_id, html_id, field, value))

                write_sections(bottom, parents)
                f.write('</li>')
        f.write('</ul>') 
                
    write_sections(sections, parents=[])
    
    f.write('''
    
    </body>
    </html>
    
    ''')
    f.close()


def make_sections(allruns, common=None):
    if common is None:
        common = {}
        
    #print('Selecting %d with %s' % (len(allruns), common))
        
    if len(allruns) == 1:
        key = allruns.keys()[0]
        value = allruns[key]
        return dict(type='sample', common=common, key=key, value=value)
    
    fields_size = [(field, len(list(allruns.groups_by_field_value(field))))
                    for field in allruns.field_names_in_all_keys()]
        
    # Now choose the one with the least choices
    fields_size.sort(key=lambda x: x[1])
    
    field = fields_size[0][0]
    division = {}
    for value, samples in allruns.groups_by_field_value(field):
        samples = samples.remove_field(field)   
        c = dict(common)
        c[field] = value
        division[value] = make_sections(samples, common=c)
        
    return dict(type='division', field=field,
                division=division, common=common)

    
    

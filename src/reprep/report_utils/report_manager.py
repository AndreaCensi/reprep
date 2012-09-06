from . import StoreResults, logger, contract
from .. import Report
from compmake import comp_stage_job_id
from compmake.structures import Promise
from compmake.utils import describe_type
import os
import time
from reprep.report_utils.store_results import frozendict


class ReportManager:
    
    def __init__(self, outdir):
        self.outdir = outdir
        self.allreports = StoreResults()
        self.allreports_filename = StoreResults()
        self.allreports_write_jobs = StoreResults()
        
    def add(self, report, report_type, **kwargs):
        if not isinstance(report, Promise):
            msg = ('ReportManager is mean to be given Promise objects, '
                   'which are the output of comp(). Obtained: %s' % describe_type(report))
            raise ValueError(msg)
        
        key = frozendict(report=report_type, **kwargs)
        
        if key in self.allreports:
            msg = 'Already added report for %s' % key
            raise ValueError(msg)
    
        dirname = os.path.join(self.outdir, report_type)
        basename = "_".join(map(str, kwargs.values()))
        filename = os.path.join(dirname, basename)
        job_id = comp_stage_job_id(report, 'write') 
        from compmake import comp
        job = comp(write_report, report, filename, job_id=job_id)
        
    
        self.allreports[key] = report
        self.allreports_filename[key] = filename + '.html'
        self.allreports_write_jobs[key] = job 
        
    def create_index_job(self):
        from compmake import comp    
        index_filename = os.path.join(self.outdir, 'report_index.html')
        for write_job in self.allreports_write_jobs.values():
            job_id = comp_stage_job_id(write_job, 'pub')
            comp(index_reports,
                 self.allreports_filename,
                 index_filename,
                 write_job,
                 job_id=job_id)
            
        #comp(index_reports, self.allreports_filename, index_filename)

    
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
        <style type="text/css">
        span.when { float: right; }
        li { clear: both; }
        </style>
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
        
        
    def write_li(k, filename):
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
        f.write('<li style="%s">%s %s</li>' % (style, a, span_when))

        
    # write the first 10
    existing.sort(key=lambda x: (-mtime(x[1])))
    nlast = min(len(existing), 10)
    last = existing[:nlast]
    f.write('<h2 id="last">Last %d reports</h2>\n' % (nlast))

    f.write('<ul>')
    for i in range(nlast):
        write_li(*last[i])
    f.write('</ul>')
    report_types = sorted(list(set(reports.field('report'))))
    

    for report_type in report_types:
        f.write('<h2 id="%s">%s</h2>\n' % (report_type, report_type))
        f.write('<ul>')
        r = reports.select(report=report_type)
        items = list(r.items()) 
        items.sort(key=lambda x: str(x[0])) # XXX use natsort   
        for k, filename in items:
            write_li(k, filename)
        f.write('</ul>')

    f.close()
#    
#def write_sections(allruns):
#    fields = allruns.field_names()
#    fields.sort() # TODO: sort
#    if not fields:
#        return
#    print fields
#    f0 = fields[0]
#    # TODO: finish
    
    

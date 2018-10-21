# -*- coding: utf-8 -*-
from contracts import contract
from reprep import MIME_RST, Report, logger
from reprep.report_utils.storing.store_results import StoreResults
from reprep.report_utils.storing.store_results_dict import StoreResultsDict
from reprep.report_utils.statistics.structures.with_description import WithDescription
from reprep.report_utils.statistics.structures.data_view import DataView


@contract(samples=StoreResults,
          rows_field=str,
          cols_fields='list[>=1](str)',
          source_descs='dict(str:WithDescription)')
def table_by_rows(id_report, samples, rows_field, cols_fields, source_descs):
    samples2 = StoreResultsDict(samples)
    
    class Missing(dict):
        def __missing__(self, key):
            logger.warning('Description for %r missing.' % key)
            d = WithDescription(name=key, symbol='\\text{%s}' % key,
                                desc=None)
            self[key] = d
            return d
        
    source_descs = Missing(source_descs)
        
    r = Report(id_report)
    data_views = [DataView.from_string(x, source_descs) for x in cols_fields]
    # data: list of list of list
    rows_field, data, reduced, display = summarize_data(samples2, rows_field, data_views)
    rows = ['$%s$' % source_descs[x].get_symbol() for x in rows_field]
    cols = ['$%s$' % x.get_symbol() for x in data_views]
    r.table('table', data=display, cols=cols, rows=rows)
    r.data('table_data', data=reduced,
           caption="Data without presentation applied.")
    r.data('table_data_source', data=data,
           caption="Source data, before reduction.")
    
    row_desc = "\n".join(['- $%s$: %s' % (x.get_symbol(), x.get_desc()) 
                          for x in map(source_descs.__getitem__, rows_field)])
    col_desc = "\n".join(['- $%s$: %s' % (x.get_symbol(), x.get_desc()) 
                          for x in data_views])
    r.text('row_desc', rst_escape_slash(row_desc), mime=MIME_RST)
    r.text('col_desc', rst_escape_slash(col_desc), mime=MIME_RST)    
    return  r


@contract(samples=StoreResultsDict, rows_field=str,
          cols_fields='list[C](DataView)',
          returns='tuple( list[R], list[R](list[C]),  '
                         'list[R](list[C]), list[R](list[C]) )')
def summarize_data(samples, rows_field, cols_fields):
    """
         returns rows, data, reduced, display 
    """
    def reduce_data(data_view, samples):
        try:
            return data_view.reduce(samples)
        except:
            msg = ('Error while applying the view\n\t%s\nto the '
                   'samples\n\t%s' % (data_view, samples))
            logger.error(msg)
            raise
            
    rows = []
    alldata = []
    for row, row_samples in samples.groups_by_field_value(rows_field):
        row_data = [reduce_data(view, row_samples) for view in cols_fields]
        alldata.append(row_data)
        rows.append(row)
        
    data = [[x[0] for x in row] for row in alldata]
    reduced = [[x[1] for x in row] for row in alldata]
    display = [[x[2] for x in row] for row in alldata]

    return rows, data, reduced, display

def rst_escape_slash(s):
    """ Replace a slash with two, useful for RST """
    return s.replace('\\', '\\\\')

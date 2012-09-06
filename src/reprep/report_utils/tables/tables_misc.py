from . import contract, logger
from .. import DataView, StoreResults, StoreResultsDict, WithDescription
from contracts import new_contract
from reprep import Report
from reprep.constants import MIME_RST
    
new_contract('DataView', DataView)
new_contract('WithDescription', WithDescription)

@contract(samples=StoreResults,
          rows_field=str,
          cols_fields='list(str|DataView)',
          source_descs='dict(str:WithDescription)')
def table_by_rows(samples, rows_field, cols_fields, source_descs):
    samples2 = StoreResultsDict(samples)
    
    class Missing(dict):
        def __missing__(self, key):
            logger.warning('Description for %r missing.' % key)
            d = WithDescription(name=key, symbol='\\text{%s}' % key,
                                desc=None)
            self[key] = d
            return d
    source_descs = Missing(source_descs)
        
    r = Report()
    data_views = [DataView.from_string(x, source_descs) for x in cols_fields]
    # data: list of list of list
    rows_field, data, reduced, display = summarize_data(samples2, rows_field, data_views)
    rows = ['$%s$' % source_descs[x].get_symbol() for x in rows_field]
    cols = ['$%s$' % x.get_symbol() for x in data_views]
    r.table('table', data=display, cols=cols, rows=rows)
    
    row_desc = "\n".join(['- $%s$: %s' % (x.get_symbol(), x.get_desc()) 
                          for x in map(source_descs.__getitem__, rows_field)])
    col_desc = "\n".join(['- $%s$: %s' % (x.get_symbol(), x.get_desc()) 
                          for x in data_views])
    r.text('row_desc', escape_slash(row_desc), mime=MIME_RST)
    r.text('col_desc', escape_slash(col_desc), mime=MIME_RST)    
    return  r

def escape_slash(s):
    """ Replace a slash with two, useful for RST """
    return s.replace('\\', '\\\\')

@contract(samples=StoreResultsDict, rows_field=str, cols_fields='list(DataView)')
#          returns='list[R](list[C](list))')
def summarize_data(samples, rows_field, cols_fields):
    """
         returns rows, data, reduced, display 
    """
    rows = []
    alldata = []
    for row, row_samples in samples.groups_by_field_value(rows_field):
        row_data = [view.reduce(row_samples) for view in cols_fields]
        alldata.append(row_data)
        rows.append(row)
        
    data = [[x[0] for x in row] for row in alldata]
    reduced = [[x[1] for x in row] for row in alldata]
    display = [[x[2] for x in row] for row in alldata]

    return rows, data, reduced, display

has_row_labels = filter(lambda x: isinstance(x, str) and len(x) > 0, table.rows)from .manager import reprep_demo


@reprep_demo
def table_demo1(r):
    cols = ['coolness', 'accuracy']
    rows = ['foo', 'bar']

    data = [[1, 2],
            [3, 4]]

    r.table('table', data=data, cols=cols, rows=rows)


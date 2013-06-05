from contracts import contract
from reprep.report_utils.statistics.tables.tables_misc import table_by_rows

__all__ = ['jobs_tables_by_sample']

@contract(cols_fields='list(str)')
def jobs_tables_by_sample(context, id_table, allstats, one_table_for_each, rows_field, cols_fields,
                source_descs={}):
    for id_case, case_runs in allstats.groups_by_field_value(one_table_for_each):
        job_id = '%s-%s' % (id_table, id_case)
        report = context.comp(table_by_rows, id_report=job_id,
                        samples=case_runs,
                        rows_field=rows_field,
                        cols_fields=cols_fields,
                        source_descs=source_descs,
                        job_id=job_id)
        attrs = case_runs.fields_with_unique_values()
        attrs[one_table_for_each] = id_case
        if rows_field in attrs:
            del attrs[rows_field]
        context.add_report(report, '%s-%s' % (id_table, id_case), **attrs)


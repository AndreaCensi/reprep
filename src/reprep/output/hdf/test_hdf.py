# -*- coding: utf-8 -*-
try:
    from . import tables
except ImportError:
    pass

else:
    from . import logger
    from reprep.output.hdf.hdf_read import report_from_hdf
    from reprep.tests import for_all_example_reports
    import os
    import shutil  # FIXME
    import tempfile
    from reprep.output.hdf.hdf1_write import to_hdf

    @for_all_example_reports
    def check_hdf_write(r):
        directory = tempfile.mkdtemp(prefix='tmp_reprep_%s' % r.nid)
        filename = os.path.join(directory, 'index.rr1.h5')
        logger.info('Written to %s' % filename)
        to_hdf(r, filename)
        r2 = report_from_hdf(filename)
        logger.info('From here ------------')
        if r != r2:
            print('-------- r ---------')
            print(r.format_tree())
            print('-------- r2 ---------')
            print(r2.format_tree())
            assert False

        shutil.rmtree(directory)
    




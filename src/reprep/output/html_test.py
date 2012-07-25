from reprep.tests.cases import for_all_example_reports
import shutil
import os
import tempfile

@for_all_example_reports
def check_to_html(r):    
    directory = tempfile.mkdtemp(prefix='tmp_reprep')
    filename = os.path.join(directory, 'index.html')
    r.to_html(filename)
    shutil.rmtree(directory)

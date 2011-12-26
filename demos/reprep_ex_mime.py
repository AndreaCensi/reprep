
from reprep import *

r = Report()

f = r.figure()

with f.plot('my_plot', mime=MIME_PDF) as pl:
    pl.plot(np.random.rand(10), np.random.rand(10))

r.to_html('reprep_ex_mime.html')

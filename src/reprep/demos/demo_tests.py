from reprep import Report
from .manager import DemoStorage


def test_all_demos():
    for id_f in DemoStorage.demos:
        demof = DemoStorage.demos[id_f]
        r = Report(id_f)
        ri = r.section(nid="%s" % demof.__name__, caption=demof.__doc__)
        demof(ri)

from reprep import Report
from reprep.demos import DemoStorage


def test_all_demos() -> None:
    for id_f in DemoStorage.demos:
        demof = DemoStorage.demos[id_f]
        r = Report(id_f)
        ri = r.section(nid="%s" % demof.__name__, caption=demof.__doc__)
        demof(ri)
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from reprep import Report
import inspect


class DemoStorage:
    demos = {}
    

def reprep_demo(f):
    ''' Decorator for declaring a reprep demo. '''
    DemoStorage.demos[f.__name__] = f
    return f


def all_demos(argv): #@UnusedVariable
    if len(argv) == 0:
        which = DemoStorage.demos.keys()
    else:
        which = argv

    print(DemoStorage.demos.keys())
    r = Report('reprep_demos')
    for id_f in which: 
        demof = DemoStorage.demos[id_f]
        ri = r.section(nid='%s' % demof.__name__, caption=demof.__doc__)
        ri.text('source', inspect.getsource(demof))
        with ri.subsection('output') as sub:
            demof(sub)

    r.to_html('reprep_demos_out/index.html')


def main():
    all_demos(sys.argv[1:])

if __name__ == '__main__':
    main()


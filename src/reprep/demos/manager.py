import sys
from reprep import Report


class DemoStorage:
    demo_list = []


def reprep_demo(f):
    ''' Decorator for declaring a reprep demo. '''
    DemoStorage.demo_list.append(f)
    return f


def all_demos(argv): #@UnusedVariable
    r = Report('reprep_demos')
    for demof in DemoStorage.demo_list:
        ri = r.section(nid='%s' % demof.__name__, caption=demof.__doc__)
        demof(ri)

    r.to_html('reprep_demos_out/index.html')


def main():
    all_demos(sys.argv)

if __name__ == '__main__':
    main()


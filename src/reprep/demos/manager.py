import sys
from reprep import Report

class DemoStorage:
    demo_list = []
    
def reprep_demo(f):
    ''' Decorator for declaring a reprep demo. '''
    DemoStorage.demo_list.append(f)
    return f

def all_demos(argv):
    r = Report('reprep_demos')
    for demo in DemoStorage.demo_list:
        ri = r.section(nid='%s' % demo.__name__,
                       caption=str(demo.__doc__)
                       )
        demo(ri)
        
    r.to_html('reprep_demos_out/index.html')
    
    
def main(): all_demos(sys.argv)
if __name__ == '__main__': main()



def set_spines_look_A(pylab, outward_offset=10):
    ''' 
        Taken from 
        http://matplotlib.sourceforge.net/examples/pylab_examples/spine_placement_demo.html
    '''
        
    ax = pylab.gca()
    for loc, spine in ax.spines.iteritems():
        if loc in ['left', 'bottom']:
            spine.set_position(('outward', outward_offset))  
        elif loc in ['right', 'top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s' % loc)

    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

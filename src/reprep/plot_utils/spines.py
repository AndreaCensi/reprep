

def set_spines_look_A(pylab, outward_offset=10,
                      linewidth=2, markersize=3, markeredgewidth=1):
    ''' 
        Taken from 
        http://matplotlib.sourceforge.net/examples/pylab_examples
        /spine_placement_demo.html
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

    for l in ax.get_xticklines() + ax.get_yticklines():
        l.set_markersize(markersize)
        l.set_markeredgewidth(markeredgewidth)

    ax.get_frame().set_linewidth(linewidth)

#for l in ax1.yaxis.get_minorticklines()+ax1.xaxis.get_minorticklines():
#
#    l.set_markersize(3) 
#
#    l.set_markeredgewidth(1.2)  

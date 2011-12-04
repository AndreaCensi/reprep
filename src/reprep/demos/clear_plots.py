from . import reprep_demo, np

def set_spines_look_A(pylab, outward_offset=10):
    ''' 
        Taken from 
        http://matplotlib.sourceforge.net/examples/pylab_examples/spine_placement_demo.html
    '''
        
    ax = pylab.gca()
    for loc, spine in ax.spines.iteritems():
        if loc in ['left', 'bottom']:
            spine.set_position(('outward', outward_offset)) # outward by 10 points
        elif loc in ['right', 'top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s' % loc)

    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

@reprep_demo
def set_spines_look_A_demo(r):
    ''' Displaying only left and bottom spines. '''
    f = r.figure()
    x = np.linspace(0, 2 * np.pi, 100)
    y = 2 * np.sin(x)         

    for off in [0, 10, 50]:
        with f.plot(
            figsize=(3, 2),
            caption='set_spines_look_A(pylab, outward_offset=%s)' % off 
        ) as pylab:
            pylab.plot(x, y)
            set_spines_look_A(pylab, outward_offset=off)

        

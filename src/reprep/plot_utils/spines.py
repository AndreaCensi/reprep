# -*- coding: utf-8 -*-
def turn_off_all_axes(pylab):
    turn_off_bottom_and_top(pylab)
    turn_off_left_and_right(pylab)


def turn_off_bottom_and_top(pylab):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['bottom', 'top']:
            spine.set_color('none')  # don't draw spine

    pylab.xticks([], [])


def turn_off_right(pylab):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['right']:
            spine.set_color('none')  # don't draw spine 
    ax.yaxis.set_ticks_position('left')


def turn_off_top(pylab):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['top']:
            spine.set_color('none')  # don't draw spine 
    ax.yaxis.set_ticks_position('bottom')


def turn_off_left_and_right(pylab):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['left', 'right']:
            spine.set_color('none')  # don't draw spine 
    pylab.yticks([], [])


def set_left_spines_outward(pylab, offset=10):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['left']:
            spine.set_position(('outward', offset))


def set_thick_ticks(pylab, markersize=3, markeredgewidth=1):
    ax = pylab.gca()
    for l in ax.get_xticklines() + ax.get_yticklines():
        l.set_markersize(markersize)
        l.set_markeredgewidth(markeredgewidth)


def set_spines_outward(pylab, outward_offset=10):
    ax = pylab.gca()
    for loc, spine in ax.spines.items():
        if loc in ['left', 'bottom']:
            spine.set_position(('outward', outward_offset))
        elif loc in ['right', 'top']:
            spine.set_color('none')  # don't draw spine
        else:
            raise ValueError('unknown spine location: %s' % loc)

    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def set_spines_look_A(pylab, outward_offset=10,
                      linewidth=2, markersize=3, markeredgewidth=1):
    ''' 
        Taken from 
        http://matplotlib.sourceforge.net/examples/pylab_examples
        /spine_placement_demo.html
    '''

    ax = pylab.gca()

    set_spines_outward(pylab, outward_offset)

    set_thick_ticks(pylab, markersize, markeredgewidth)

    try:
        #         f = pylab.gcf()
        #         ax.get_frame().set_linewidth(linewidth)

        [i.set_linewidth(linewidth) for i in ax.spines.items()]

    except BaseException as e:
        print('set_linewidth() not working in matplotlib 1.3.1: %s' % e)

    # ax.get_frame().set_linewidth(linewidth)

# for l in ax1.yaxis.get_minorticklines()+ax1.xaxis.get_minorticklines():
#
#    l.set_markersize(3) 
#
#    l.set_markeredgewidth(1.2)

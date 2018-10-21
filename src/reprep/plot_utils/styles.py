# -*- coding: utf-8 -*-
from reprep.plot_utils.spines import set_spines_look_A

ieee_colsize = 1.57 * 2


def ieee_spines(pylab):
    set_spines_look_A(pylab, outward_offset=5,
                      linewidth=1, markersize=2, markeredgewidth=0.5)


def ieee_fonts(pylab):
    # See http://matplotlib.sourceforge.net
    # /users/customizing.html#matplotlibrc-sample
    params = {
        'axes.labelsize': 8,
        #           'text.fontsize': 8,
        'font.size': 8,
        'legend.fontsize': 8,
        'xtick.labelsize': 6,
        'ytick.labelsize': 6,
        'lines.markersize': 1,
        'lines.markeredgewidth': 0,
        # 'axes.color_cycle': ['k', 'm', 'g', 'c', 'm', 'y', 'k'],
        'legend.fancybox': True,
        'legend.frameon': False,
        'legend.numpoints': 1,
        'legend.markerscale': 2,
        'legend.labelspacing': 0.2,
        'legend.columnspacing': 1,
        'legend.borderaxespad': 0.1
        #          'font.family': 'Times New Roman',
        #          'font.serif': ['Times New Roman', 'Times'],
        #          'font.size': 8
        #      'text.usetex': True
    }
    pylab.rcParams.update(params)

    from matplotlib import rc
    # cmr10 works but no '-' sign
    rc('font', **{'family': 'serif',
                  'serif': ['Bitstream Vera Serif', 'Times New Roman',
                            'Palatino'],
                  'size': 8.0})


# rc('font', **{'family': 'cmr10',
#                 'serif': ['cmr10', 'Times New Roman', 'Palatino'],
#                  'size': 8.0})


def style_ieee_halfcol_xy(pylab, ratio=3.0 / 4):
    ''' 
        Note: not sure if should be called before plotting, or after.
        Find out and write it here.
        
        ratio=1 to have a square one
    '''
    f = pylab.gcf()
    f.set_size_inches((ieee_colsize / 2, ieee_colsize / 2 * ratio))
    ieee_fonts(pylab)
    ieee_spines(pylab)


def style_ieee_fullcol_xy(pylab, ratio=3.0 / 4):
    f = pylab.gcf()
    f.set_size_inches((ieee_colsize, ieee_colsize * ratio))
    ieee_fonts(pylab)
    ieee_spines(pylab)

#  # update the font size of the x and y axes
#  fontsize=16
#  pylab.plot([1,2,3],[4,5,6])
#  ax = pylab.gca()
#  for tick in ax.xaxis.get_major_ticks():
#    tick.label1.set_fontsize(fontsize)
#  for tick in ax.yaxis.get_major_ticks():
#    tick.label1.set_fontsize(fontsize)
# Can also update the tick label font using set_fontname('Helvetica')
# See also the Text class in the matplotlib api doc.

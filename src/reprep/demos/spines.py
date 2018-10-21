# -*- coding: utf-8 -*-
import numpy as np
from reprep.plot_utils import set_spines_look_A, set_thick_ticks

from .manager import reprep_demo


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


@reprep_demo
def set_spines_look_B_Demo(r):
    f = r.figure()
    x = np.linspace(0, 2 * np.pi, 100)
    y = 2 * np.sin(x)         

    for marker in [0, 1, 2, 3, 4, 5]:
        with f.plot(
            figsize=(3, 2),
            caption='set_spines_look_A(pylab, outward_offset=%s)' % marker  
        ) as pylab:
            pylab.plot(x, y)
            set_thick_ticks(pylab)
            ax = pylab.gca()
            ticks = ax.xaxis.get_majorticklines() 
            for t in ticks:
                t.set_marker(marker)

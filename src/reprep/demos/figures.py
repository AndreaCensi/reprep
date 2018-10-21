# -*- coding: utf-8 -*-
from reprep.demos.manager import reprep_demo
import numpy as np

@reprep_demo
def demo_figure1(r):
    # You don't need to create a figure --- RepRep will figure it out.
    nplots = 4
    for k in range(nplots):
        # Reprep creates "figure1" in r to hold your plots
        with r.plot('plot-%d' % k) as pylab:
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x * (k + 1))
            pylab.plot(x, y)


@reprep_demo
def demo_figure2(r):
    # Create first a figure as a container for plots.
    nplots = 4
    f = r.figure(cols=nplots, caption='My figure')

    for k in range(nplots):
        # You can add directly the plot to the figure
        with f.plot('plot-%d' % k) as pylab:
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x * (k + 1))
            pylab.plot(x, y)

@reprep_demo
def demo_figure3(r):
    # Create first a figure as a container for plots.
    nplots = 4
    f = r.figure(cols=nplots, caption='My figure')

    for k in range(nplots):
        # Note you can add the plot to the report "r"
        with r.plot('plot-%d' % k) as pylab:
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x * (k + 1))
            pylab.plot(x, y)
        # and then add it explicitly to the figure
        f.sub(r.last())


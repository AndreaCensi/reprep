# -*- coding: utf-8 -*-
import numpy as np

from .manager import reprep_demo


@reprep_demo
def demo_layout33(r):
    demo_columns(r, nplots=3, ncols=3)


@reprep_demo
def demo_layout34(r):
    demo_columns(r, nplots=3, ncols=4)


@reprep_demo
def demo_layout65(r):
    demo_columns(r, nplots=6, ncols=5)


def demo_columns(r, nplots, ncols):
    f = r.figure(cols=ncols)

    for k in range(nplots):
        with f.plot() as pylab:
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x * (k + 1))
            pylab.plot(x, y)


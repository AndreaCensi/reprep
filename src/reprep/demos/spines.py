from . import reprep_demo, np
from reprep.plot_utils.spines import set_spines_look_A


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

        

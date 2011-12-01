from reprep import Report
from reprep.graphics import filter_colormap
from reprep.graphics import get_solid
import numpy as np


def get_test_bar(shape=(100, 10)):
    bar = np.vstack([np.linspace(-0.1, 1.2, shape[0])] * shape[1]).T
    pos = bar > 1
    neg = bar < 0
    nan = bar > 1.1
    bar[pos] = +np.Inf
    bar[neg] = -np.Inf
    bar[nan] = np.NaN
    print bar
    return bar
    
def diagflip(x):
    return np.transpose(x, (1, 0, 2))
    
def demo_colormaps():
    x = get_test_bar()
    cmaps = ['Reds', 'jet', 'Accent']
    
    r = Report()
    
    for cmap in cmaps:
        f = r.figure(cmap)
        properties = {}
        rgba = filter_colormap(x, cmap, properties=properties)
        f.data_rgb('result', diagflip(rgba))
        f.data_rgb('colorbar', diagflip(properties['color_bar']))
        f.data_rgb('nan_color', get_solid((20, 20), properties['nan_color']))
        f.data_rgb('inf_color', get_solid((20, 20), properties['inf_color']))
        f.data_rgb('flat_color', get_solid((20, 20), properties['flat_color']))
        
#        with f.plot('colorbar') as pl:
#            pl.imshow(properties['color_bar'].T)
        
    
    r.to_html('reprep_demo_colormaps.html')
    
    
if __name__ == '__main__':
    demo_colormaps()

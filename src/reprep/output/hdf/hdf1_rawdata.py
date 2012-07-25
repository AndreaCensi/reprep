from tables.flavor import flavor_of
from StringIO import StringIO
import cPickle
import tables

def write_python_data(parent, name, mime, data):
    hf = parent._v_file
    group = hf.createGroup(parent, name)
    hf.createArray(group, 'mime', mime)
    try:
        flavor_of(data)
        ok_pytables = True
    except:
        ok_pytables = False
    
    if ok_pytables: 
        hf.createArray(group, 'value', data)
        serialized = 'pytables'
    else:
        serialized = 'pickle'
        s = StringIO()
        cPickle.dump(data, s, protocol=2)
        hf.createVLArray(group, 'pickle', tables.VLStringAtom(), filters=None)
        group.pickle.append(s.getvalue())    
    group._v_attrs['reprep_data_format'] = serialized
    
    
def read_python_data(parent, name):
    """ Returns MIME, object """
    group = parent._v_children[name]
    reprep_data_format = group._v_attrs['reprep_data_format']
    mime = group.mime.read()
    if reprep_data_format == 'pytables':
        data = group.value.read()
    elif reprep_data_format == 'pickle':
        pickled = group.pickle[0]
        data = cPickle.load(StringIO(pickled))
    else: 
        raise ValueError(format)
    return mime, data

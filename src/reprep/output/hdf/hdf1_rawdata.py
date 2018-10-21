# -*- coding: utf-8 -*-
from six.moves import cPickle
from six import StringIO

from reprep import logger
from contracts import describe_type, describe_value
from reprep.output.hdf import get_tables

__all__ = ['write_python_data', 'read_python_data']


def write_python_data(parent, name, mime, data):
    tables = get_tables()
    from tables.flavor import flavor_of
    hf = parent._v_file
    group = hf.createGroup(parent, name)
    hf.createArray(group, 'mime', mime)
    try:
        flavor_of(data)
        ok_pytables = True
    except:
        ok_pytables = False
    
    # 2014-01-02 XXX this is a hack
    if data == []:
        ok_pytables = False
        
    if ok_pytables: 
        try:
            hf.createArray(group, 'value', data)
        except:
            msg = 'Error while writing python data'
            msg += '\n parent: %s' % parent
            msg += '\n name: %s' % name
            msg += '\n mime: %s' % mime
            msg += '\n data: %s' % describe_type(data)
            msg += '\n       %s' % describe_value(data)
            msg += '\n flavor: %s' % flavor_of(data)
            msg += '\nraw:\n%s' % data.__repr__()
            logger.error(msg)
            raise
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

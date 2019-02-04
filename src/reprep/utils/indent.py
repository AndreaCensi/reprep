# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def indent(s, prefix):
    if '\n' in prefix:
        raise ValueError('Invalid prefix.')
    lines = s.split('\n')
    lines = ['%s%s' % (prefix, line) for line in lines]
    return '\n'.join(lines)

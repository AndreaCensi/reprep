# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# natsort.py: Natural string sorting.
# ---------------------------------------------------------

# By Seo Sanghyeon.  Some changes by Connelly Barnes.


def try_int(s):
    "Convert to integer if possible."
    try:
        return int(s)
    except:
        return s


def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    s = str(s)  # convert everything to string
    return tuple(map(try_int, re.findall(r'(\d+|\D+)', s)))

#
# def cmp2(a, b):
#     return (a > b) - (a < b)


#
# def natcmp(a, b):
#     "Natural string comparison, case sensitive."
#     return cmp2(natsort_key(a), natsort_key(b))

#
# def natcasecmp(a, b):
#     "Natural string comparison, ignores case."
#     return natcmp(a.lower(), b.lower())
#

#
# def natsort(seq, compare=natcmp):
#     "In-place natural string sort."
#     seq.sort(key=compare)


def natsorted(seq):
    "Returns a copy of seq, sorted by natural string sort."
    # convert set -> list
    return sorted(list(seq), key=natsort_key)

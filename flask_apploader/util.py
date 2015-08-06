# -*- coding: UTF-8 -*-


def ensure_iterable(v):
    if hasattr(v, '__iter__'):
        return v
    else:
        return [v]

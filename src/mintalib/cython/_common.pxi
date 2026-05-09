# common imports to all pxi files

from libc cimport math
from libc.math cimport isnan

cdef double NAN = float('nan')

import numpy as np

from enum import IntEnum

from collections import namedtuple
from types import MappingProxyType



def check_size(*args):
    """check all series have the same size and return the size"""

    xs, *others = args

    cdef long size = xs.size
    for s in others:
        if s.size != size:
               raise ValueError("Different sizes!")
    return size



def add_metadata(*, same_scale: bool = None, output_names: list | tuple = None):
    """update function with metadata"""

    if same_scale is not None:
        same_scale = bool(same_scale)

    if output_names is not None:
        output_names = tuple(output_names)

    metadata = dict(same_scale=same_scale, output_names=output_names)
    metadata = { k: v for k, v in metadata.items() if v is not None}

    def wrapper(func):
        func.metadata = MappingProxyType(metadata)
        return func

    return wrapper


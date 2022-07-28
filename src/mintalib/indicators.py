from . import core

__all__ = []

for name in [n for n in dir(core) if n.isupper() and n.isalpha()]:
    globals()[name] = getattr(core, name)
    __all__.append(name)

del core
del name

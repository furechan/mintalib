from . import core

for name in [n for n in dir(core) if n.startswith("calc_")]:
    globals()[name[5:]] = getattr(core, name)

del core
del name

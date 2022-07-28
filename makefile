# makefile should be tab indented!

name = mintalib
version = 0.0.1

build: FORCE
	-jupyter notebook stop 2> nul
	cythonize -3 ./**/*.pyx
	python setup.py build_ext --inplace

clean: FORCE
    del /s /q src\*.c src\*.pyd

dist: FORCE
    python -mbuild --sdist .

dump: FORCE
    tar -tvf dist/$(name)-$(version).tar.gz

install: FORCE
	python setup.py develop


remove: FORCE
	python setup.py develop -u


FORCE:

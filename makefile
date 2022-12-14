--inplace# makefile should be tab indented!

name = mintalib
version = 0.0.1

build: FORCE
	-jupyter notebook stop 2> nul
	cythonize -3 ./**/*.pyx
	python3 setup.py build_ext --inplace
	python3 -m runpynb scripts\make-wrappers.ipynb

clean: FORCE
	python3 setup.py clean

dist: FORCE
	python3 -mbuild --sdist .

dump: FORCE
	tar -tvf dist/$(name)-$(version).tar.gz

install: FORCE
	python3 setup.py develop

remove: FORCE
	python3 setup.py develop -u

tox: FORCE
	tox --workdir %USERPROFILE%\Parking\$(name).tox

upload: FORCE
	twine upload dist/*

FORCE:

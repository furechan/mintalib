from setuptools import setup, find_packages, Extension

from pathlib import Path

srcdir = 'src'
name = "mintalib"
version = '0.0.1'
url = "https://github.com/furechan/mintalib-proto"


def make_extension(path):
    name = path.relative_to(srcdir).with_suffix("").as_posix().replace('/', '.')
    return Extension(name=name, sources=[str(path)])


packages = find_packages(srcdir)

extensions = [make_extension(f) for f in Path(srcdir).rglob('*.c')]

classifiers = [
    "Topic :: Scientific/Engineering",
    "Development Status :: 2 - Pre-Alpha",
    "Programming Language :: Cython",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]

setup(
    url=url,
    name=name,
    version=version,
    packages=packages,
    ext_modules=extensions,
    classifiers=classifiers,
    package_dir={'': srcdir},

    include_package_data=True,

    author="furechan",
    author_email="furechan@xsmail.com",

    install_requires=["numpy", "pandas"],
    tests_require=["pytest", "talib"],
)

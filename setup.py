import re

from pathlib import Path
from setuptools import setup, find_packages, Extension


def get_version(path):
    data = Path(__file__).parent.joinpath(path).read_text()
    match = re.search(
        r"^ __version__ \s* = \s* (['\"]) ([^'\"]+) \1 \s* $",
        data, re.X | re.MULTILINE)
    if match:
        return match.group(2)
    raise ValueError(f"Cound not get version from {path}")


def make_extension(path):
    name = path.relative_to(srcdir).with_suffix("").as_posix().replace('/', '.')
    return Extension(name=name, sources=[str(path)])


root = Path(__file__).parent
long_description = root.joinpath("output/README.md").read_text()


srcdir = 'src'
name = "mintalib"
url = "https://github.com/furechan/mintalib"
description = "Minimalist Technical Analysis Library for Python"

version = get_version("src/mintalib/__init__.py")

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
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="furechan",
    author_email="furechan@xsmail.com",
    python_requires=">=3.8",
    install_requires=["numpy", "pandas"],
    tests_require=["pytest", "ta-lib"],
)

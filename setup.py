import re
import posixpath

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


def process_readme(file, project_url, branch="main", verbose=False):
    def replace(m):
        exclam, alt, url = m.groups()
        ftype = "raw" if exclam else "blob"
        if url.startswith("/"):
            url = posixpath.join(project_url, ftype, branch, url[1:])
            text = f"{exclam}[{alt}]({url})"
            if verbose:
                print("mapping", m.group(0), "->", text)
        else:
            text = m.group(0)
        return text

    source = file.read_text()
    result = re.sub(r"(?x)(\!?)\[([^]]*)\]\(([^)]+)\)", replace, source)
    return result


def make_extension(path):
    name = path.relative_to(srcdir).with_suffix("").as_posix().replace('/', '.')
    return Extension(name=name, sources=[str(path)])


srcdir = 'src'
name = "mintalib"
url = "https://github.com/furechan/mintalib"
description = "Minimalist Technical Analysis Library for Python"

root = Path(__file__).parent
readme = root.joinpath("README.md")
long_description = process_readme(readme, project_url=url)

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
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="furechan",
    author_email="furechan@xsmail.com",
    python_requires=">=3.8",
    install_requires=["numpy", "pandas"],
    tests_require=["pytest"],

    package_dir={'': srcdir},
    package_data={'mintalib.testing': ['data/*.csv']},
    include_package_data=True,
)

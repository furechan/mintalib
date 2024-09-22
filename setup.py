import sys
from pathlib import Path
from setuptools import setup, find_packages, Extension

srcdir = "src"
package_dir = {"": srcdir}
packages = find_packages(where=srcdir)
extra_compile_args = []

# Extra compilation flags to suppress cython related warnings on MacOS ...
if sys.platform == "darwin":
    extra_compile_args = ["-Wno-unreachable-code", "-Wno-deprecated-declarations"]


def make_extension(path):
    name = path.relative_to(srcdir).with_suffix("").as_posix().replace("/", ".")
    return Extension(
        name=name, sources=[str(path)], extra_compile_args=extra_compile_args
    )


# ext_modules = [make_extension(f) for f in Path(srcdir).rglob("*.pyx")]
ext_modules = [make_extension(f) for f in Path(srcdir).rglob("*.c")]

setup(
    packages=packages,
    package_dir=package_dir,
    ext_modules=ext_modules,
)

""" script to generate code for the functions sub-module """

import ast
import argparse

from pathlib import Path

from mintalib import core

pkgdir = Path(__file__).joinpath("../../src/mintalib").resolve(strict=True)


def generate_imports():
    buffer = "# Do not edit! file generated automatically. see make-functions.py\n\n"
    buffer += "''' Mintalib functions library '''\n\n"
    for name in [n for n in dir(core) if n.startswith("calc_")]:
        alias = name.partition("_")[2]
        buffer += f"from .core import {name} as {alias}\n"

    return buffer


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(verbose=False)
    parser.add_argument('-v', '--verbose', action="store_true", help="display generated code")

    options = parser.parse_args()

    target = pkgdir / "functions.py"
    source = generate_imports()

    ast.parse(source, filename='<unknown>', mode='exec')

    print(f"Updating {target} ...")
    target.write_text(source)

    if options.verbose:
        print(source)


if __name__ == "__main__":
    main()

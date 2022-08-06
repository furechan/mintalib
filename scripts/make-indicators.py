""" script to generate code for the indicators sub-module """

import ast
import argparse

from pathlib import Path

from mintalib import core

from pprint import pformat

pkgdir = Path(__file__).joinpath("../../src/mintalib").resolve(strict=True)


def generate_imports():
    buffer = "# Do not edit! file generated automatically. see make-indicators.py\n\n"
    buffer += "''' Mintalib indicators library '''\n\n"
    names = [n for n in dir(core) if n.isupper() and n.isalpha()]
    for name in names:
        buffer += f"from .core import {name}\n"

    names = pformat(names, compact=True, indent=0)
    buffer += f"\n__all__ = {names}\n"

    return buffer


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(verbose=False)
    parser.add_argument('-v', '--verbose', action="store_true", help="display generated code")

    options = parser.parse_args()

    target = pkgdir / "indicators.py"
    source = generate_imports()

    ast.parse(source, filename='<unknown>', mode='exec')

    print(f"Updating {target} ...")
    target.write_text(source)

    if options.verbose:
        print(source)


if __name__ == "__main__":
    main()

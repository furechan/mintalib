""" local project utility """

from pathlib import Path

root = Path(__file__).parent.parent.resolve()

srcdir = root.joinpath("src").resolve(strict=True)
pkgdir = root.joinpath("src/mintalib").resolve(strict=True)

def save_output(fname, data, *, encoding='utf-8', verbose=True):
    """ save text to a file in the output folder """

    output = root.joinpath("output").resolve(strict=True)
    file = output / fname
    if verbose:
        print(f"Updating {fname} ...")
    file.write_text(data, encoding=encoding)


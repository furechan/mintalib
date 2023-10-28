""" local project settings """

from pathlib import Path

ROOTDIR = Path(__file__).parent.parent.resolve()

SRCDIR = ROOTDIR.joinpath("src").resolve(strict=True)
TESTDIR = ROOTDIR.joinpath("tests").resolve(strict=True)
PKGDIR = ROOTDIR.joinpath("src/mintalib").resolve(strict=True)


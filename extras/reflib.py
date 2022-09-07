""" combined function imports from all tests """

import pkgutil
import logging

from pathlib import Path

test_folder = Path.cwd().joinpath('../tests').resolve(strict=True)


def import_test_modules():
    logger = logging.getLogger(__name__)
    exports = globals().setdefault('__all__', [])

    for loader, module_name, is_pkg in pkgutil.walk_packages([str(test_folder)]):
        logger.info("loading %s ...", module_name)
        module = loader.find_module(module_name).load_module(module_name)
        for k, v in vars(module).items():
            if k.startswith("ref_"):
                exports.append(k)
                globals()[k] = v


import_test_modules()

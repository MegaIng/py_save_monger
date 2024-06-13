from pathlib import Path
from typing import Iterable, List

import setuptools
from nimporter import Nimporter


class RestrictedNimporter(Nimporter):
    @classmethod
    def _find_extensions(cls, path: Path, exclude_dirs: Iterable = set()) -> List[Path]:
        return list(path.rglob("nim_save_monger.nim"))


setuptools.setup(
    ext_modules=RestrictedNimporter.build_nim_extensions()
)

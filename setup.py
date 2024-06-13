import sys

import setuptools
from nimporter import get_nim_extensions, LINUX, MACOS, WINDOWS, ic, nexporter

from pprint import pp


def fixed_prevent_win32_max_path_length_error(path) -> None:
    """
    Nim generates C files that contain `@` symbols to encode the original path
    to the Nim module. However, there are 2 problems with this:
        1. They contain the user's private directory structure
        2. They cause compilation to fail on Win32 MSVC (max path length 260)

    This function just removes the encoded path and adds a prefix so that users
    of Nimporter can tell who made that change.

    Turns this:
        @m..@s..@s..@s..@s..@s..@sUsers@s<USERNAME>@s.nimble@spkgs@snimpy-0.2.0@snimpy@spy_utils.nim.c
    Into:
        NIMPORTER@nimpy-0.2.0@nimpy@py_utils.nim.c

    That's a lot less characters!
    """

    def is_valid_identifier(string: str) -> bool:
        import re
        match = re.search('^[A-Za-z_][A-Z-a-z0-9_\\-]*', string)
        return match and len(match.string) == len(string)

    def is_semver(string: str) -> bool | str:
        try:
            lib_name, lib_version, *hsh = string.rsplit('-', maxsplit=2)
            assert is_valid_identifier(lib_name)

            major, minor, patch = lib_version.split('.')
            assert major.isdigit()
            assert minor.isdigit()
            assert patch.isdigit()
            if hsh:
                assert hsh[0].isalnum()

            return f"{lib_name}-{major}.{minor}.{patch}"
        except:
            return False

    for item in path.iterdir():
        if item.is_file() and item.name.startswith('@m'):

            # Bare module. Module not from library dependency
            if '@s' not in item.name:
                mod_name = item.name.replace('@m', '')

            # Module from a library dependency. Find the package the module
            # belongs to (if any)
            else:
                segments = item.name.replace('@m', '').split('@s')

                for index, segment in reversed(list(enumerate(segments))):
                    if segment := is_semver(segment):
                        mod_name = '@'.join([segment] + segments[index + 1:])
                        break
                else:
                    mod_name = item.name.replace('@m', '')

            new_name = ic(f'NIMPORTER@{mod_name}')
            target = item.with_name(new_name)
            assert not target.exists(), (item, new_name)
            item.replace(target)


nexporter.prevent_win32_max_path_length_error = fixed_prevent_win32_max_path_length_error
print("-" * 100, sys.argv)
nim_extensions = get_nim_extensions([LINUX, MACOS, WINDOWS])
setuptools.setup(
    ext_modules=nim_extensions
)

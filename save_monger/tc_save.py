from __future__ import annotations

import os.path
import platform
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TCSave:
    schematics: Path

    @classmethod
    def default_profile(cls) -> TCSave:
        match platform.system():
            case 'Linux':
                return TCSave(Path("~/.local/share/godot/app_userdata/Turing Complete/schematics").expanduser())
            case 'Darwin':
                return TCSave(Path("~/Library/Application Support/Godot/app_userdata/Turing Complete/schematics").expanduser())
            case 'Windows':
                return TCSave(Path(os.path.expandvars(r"%AppData%\godot\app_userdata\Turing Complete\schematics")))
            case other:
                raise ValueError(f"Unrecognized platform: {other!r}")

    def get_path(self, level: str, save_name: str = "Default") -> Path:
        return self.schematics / level / save_name / "circuit.data"

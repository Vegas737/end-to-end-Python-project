from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

@dataclass
class Config:
    raw: Dict[str, Any]

    @property
    def variant_id(self) -> str:
        return str(self.raw.get("variant_id", ""))

    @property
    def source_type(self) -> str:
        return str(self.raw.get("source_type", ""))

    @property
    def api(self) -> Dict[str, Any]:
        return dict(self.raw.get("api", {}))

def load_config(path: str | Path) -> Config:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(raw=raw)

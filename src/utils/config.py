from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import yaml


def load_config(path: str | Path) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if cfg is None:
        raise ValueError(f"Configuration file is empty: {path}")
    return cfg


def ensure_output_dir(cfg: Dict[str, Any]) -> Path:
    """Create and return the experiment output directory."""
    output_dir = Path(cfg.get("output_dir", "outputs/experiment"))
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

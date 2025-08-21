
from __future__ import annotations
import os, importlib.util, traceback
from typing import Dict, Any, List

MODULE_DIR = os.path.join(os.path.dirname(__file__), "..", "modules")
os.makedirs(MODULE_DIR, exist_ok=True)

class LoadedModule:
    def __init__(self, name: str, module, error: str | None = None):
        self.name = name; self.module = module; self.error = error

def discover_modules() -> List[str]:
    return [os.path.join(MODULE_DIR, f) for f in os.listdir(MODULE_DIR) if f.endswith(".py") and not f.startswith("_")]

def load_module(path: str) -> LoadedModule:
    name = os.path.splitext(os.path.basename(path))[0]
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)  # type: ignore
        return LoadedModule(getattr(mod, "MODULE_NAME", name), mod, None)
    except Exception:
        return LoadedModule(name, None, traceback.format_exc())

def load_all() -> List[LoadedModule]:
    return [load_module(p) for p in discover_modules()]

def apply_modules(mods: List[LoadedModule], outputs: Dict[str,str], context: Dict[str,Any]) -> Dict[str,str]:
    res = dict(outputs)
    for lm in mods:
        if lm.module and hasattr(lm.module, "apply"):
            try: res = lm.module.apply(res, context) or res
            except Exception: pass
    return res

#!/usr/bin/env python3
"""
Loader for Ollama Godmode jailbreaking scripts.
Use this to import all godmode functions into the current namespace.

Usage:
    exec(open("skills/ollama-godmode/scripts/load_godmode.py").read())

    # Now you have access to:
    # - auto_jailbreak_ollama()     — test strategies against a model
    # - race_ollama_models()        — race multiple models in parallel
    # - score_response()            — score a response
    # - is_refusal()                — check if a response is a refusal
    # - count_hedges()              — count hedge patterns
    # - generate_variants()         — generate Parseltongue obfuscations
    # - obfuscate_query()           — obfuscate a single query
    # - escalate_encoding()         — escalate encoding level
    # - list_ollama_models()        — list available models
"""

import os
from pathlib import Path

# Determine this script's directory
_LOADER_DIR = Path(__file__).resolve().parent

# Scripts to load, in order
_SCRIPTS = ["parseltongue.py", "godmode_race.py", "auto_jailbreak.py"]

# Load scripts into the calling namespace
import inspect as _inspect
_caller_globals = _inspect.stack()[0][0].f_globals if len(_inspect.stack()) > 0 else globals()

for _script_name in _SCRIPTS:
    _script_path = _LOADER_DIR / _script_name
    if _script_path.exists():
        exec(compile(open(_script_path).read(), str(_script_path), 'exec'), _caller_globals)

# Clean up internal variables
del _LOADER_DIR, _SCRIPTS, _script_name, _script_path, _inspect, _caller_globals
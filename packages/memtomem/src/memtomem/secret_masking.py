"""Shared configuration secret masking for CLI and MCP output surfaces."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

MASK = "***"


def is_secret_key(key: str) -> bool:
    """Return whether a configuration field name carries secret material."""
    normalized = key.casefold()
    return normalized in {"api_key", "secret"} or normalized.endswith("_secret_key")


def mask_secrets(value: Any) -> Any:
    """Recursively mask non-empty secret fields without changing shape."""
    if isinstance(value, dict):
        result = deepcopy(value)
        for key, child in result.items():
            if is_secret_key(str(key)) and child not in (None, ""):
                result[key] = MASK
            else:
                result[key] = mask_secrets(child)
        return result
    if isinstance(value, list):
        return [mask_secrets(item) for item in value]
    if isinstance(value, tuple):
        return tuple(mask_secrets(item) for item in value)
    return value

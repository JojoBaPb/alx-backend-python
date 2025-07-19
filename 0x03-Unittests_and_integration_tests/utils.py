#!/usr/bin/env python3
"""Module for accessing values in nested maps."""
from typing import Any, Dict, Tuple


def access_nested_map(nested_map: Dict, path: Tuple[Any]) -> Any:
    """
    Access a value in a nested dictionary via a path of keys.

    Args:
        nested_map: A dictionary potentially containing other dictionaries.
        path: A tuple of keys that represents the access path.

    Returns:
        The value at the end of the path.

    Raises:
        KeyError: If any key in the path is missing.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


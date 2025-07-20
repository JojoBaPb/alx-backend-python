#!/usr/bin/env python3
"""
Utils module with access_nested_map and memoize functions.
"""

from functools import wraps
from typing import Any, Dict, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a nested map with a sequence of keys.

    Args:
        nested_map (dict): The dictionary to traverse.
        path (sequence): A sequence of keys indicating the path.

    Returns:
        The value located at the end of the path.

    Raises:
        KeyError: If any key in the path is missing.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def memoize(method):
    """
    Decorator that caches method results.

    Args:
        method: Method to be memoized.

    Returns:
        Wrapper function with caching.
    """
    attr_name = "_{}".format(method.__name__)

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper


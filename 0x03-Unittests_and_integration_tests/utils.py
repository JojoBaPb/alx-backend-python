#!/usr/bin/env python3
"""A set of utility functions for accessing nested maps and memoization."""
from typing import Any, Dict, Tuple
from functools import wraps


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


def memoize(method):
    """Decorator that caches method results."""
    attr_name = "_{}".format(method.__name__)

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return wrapper

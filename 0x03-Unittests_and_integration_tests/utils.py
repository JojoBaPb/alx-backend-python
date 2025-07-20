#!/usr/bin/env python3
"""Module for accessing values in nested maps."""
from typing import Any, Dict, Tuple

"""Module for fetching JSON data from a URL"""
"""Utilities for testing memoization."""
import requests
from functools import wraps

def get_json(url):
    """Fetches JSON response from a URL"""
    response = requests.get(url)
    return response.json()

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
    """Decorator that caches method results"""
    attr_name = "_{}".format(method.__name__)

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    
    return wrapper

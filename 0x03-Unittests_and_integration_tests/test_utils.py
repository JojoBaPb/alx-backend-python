#!/usr/bin/env python3

"""Unit tests for utils.access_nested_map"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

"""Unit tests for utils.get_json"""
from unittest.mock import patch, Mock
from utils import get_json

class TestGetJson(unittest.TestCase):
    """Test the get_json function"""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test that get_json returns expected JSON payload"""
        test_url = "http://example.com"
        expected_payload = {"payload": True}

        # Configure the mock to return a response with .json() method
        mock_response = Mock()
        mock_response.json.return_value = expected_payload
        mock_get.return_value = mock_response

        # Run the function
        result = get_json(test_url)

        # Assertions
        self.assertEqual(result, expected_payload)
        mock_get.assert_called_once_with(test_url)

class TestAccessNestedMap(unittest.TestCase):
    """Test the access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError on invalid path"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


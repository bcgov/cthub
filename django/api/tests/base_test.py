"""
Default instructions for the test cases
"""
from django.test import TestCase


class BaseTestCase(TestCase):
    """
    Load the following fixtures for each test case
    """
    fixtures = [
    ]

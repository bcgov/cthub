"""
Default instructions for the test cases
"""
from django.test import TestCase


class BaseTestCase(TestCase):
    """
    Load the following fixtures for each test case
    """
    fixtures = [
        'teams.json',
        'tests/players.json',
        'tests/rushing_stats.json'
    ]

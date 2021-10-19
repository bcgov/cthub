"""
Test Suite for Rushing Stats
"""
import json
from django.test import Client

from api.models.player import Player
from api.services.rushing_stats import import_from_json
from api.tests.base_test import BaseTestCase


class TestRushingStats(BaseTestCase):
    def test_import_from_json(self):
        """
        Tests the import function by passing a json object and
        seeing if it actually creates the record.
        """
        import_from_json(json.loads(json.dumps([{
            "Player": "Test Player",
            "Team": "JAX",
            "Pos": "RB",
            "Att": 1,
            "Att/G": 1,
            "Yds": 1,
            "Avg": 1,
            "Yds/G": 1,
            "TD": 0,
            "Lng": "1",
            "1st": 1,
            "1st%": 1,
            "20+": 1,
            "40+": 1,
            "FUM": 1
        }])))

        player = Player.objects.get(
            first_name='Test',
            last_name='Player'
        )

        self.assertEqual(player.team.t_code, 'JAX')

    def test_order_by(self):
        """
        Testing by ordering by last name, first name in descending order
        The test fixture only contains 2 players: Joe Banyard and Shaun Hill.
        So Shaun should show up first
        """
        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?ordering=-player__last_name,player__first_name'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Shaun')

    def test_order_by_team(self):
        """
        Follow-up test to order by and see if we can go into a related field
        that's deeper than the player name.
        Joe should list first for being with Jacksonville vs Minnesota
        """
        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?ordering=-player__team__t_name'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Shaun')

    def test_filter_by_player(self):
        """
        Testing filter by player name.
        Player's name are stored in separate first name and last name columns,
        Passing Shaun or partial matches like Ban should result with the
        related records.
        """
        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?player=Shaun'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Shaun')

        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?player=Ban'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Joe')

    def test_filter_by_position(self):
        """
        Testing filter by position.
        """
        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?player__position=QB'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Shaun')

    def test_filter_by_team(self):
        """
        Testing filter by team.
        """
        web_client = Client()
        response = web_client.get(
            '/api/rushing-stats?player__team__t_code=JAX'
        )

        row = response.data.get('results')[0]
        self.assertEqual(row.get('player').get('first_name'), 'Joe')

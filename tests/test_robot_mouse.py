import unittest

from torch import TupleType
from robot_mouse import robot_mouse


class TestRobotMouse(unittest.TestCase):

    def test_make_grid(self):
        grid = robot_mouse.make_grid(5)
        self.assertEqual(len(grid), 5)

    def test_get_cheese(self):
        grid = [
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', "🧱", "🧱", '🧱', '🧱', '🧱'],
            ['🧱', "🧱", "🧱", '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
        ]
        cheese_list = robot_mouse.get_cheese(grid)
        self.assertIsInstance(cheese_list, list)
        self.assertIsInstance(cheese_list[0], tuple)
        self.assertEqual(len(cheese_list), 5)
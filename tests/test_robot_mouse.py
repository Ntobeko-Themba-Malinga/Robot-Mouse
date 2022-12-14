import os
import unittest
from robot_mouse import robot_mouse


class TestRobotMouse(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.grid = [
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', "🧱", "🧱", '🧱', '🧱', '🧱'],
            ['🧱', "🧱", "🐁", '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
        ]

    def test_make_grid(self):
        grid = robot_mouse.make_grid(5)
        self.assertEqual(len(grid), 5)

    def test_get_cheese(self):
        cheese_list = robot_mouse.get_cheese(self.grid)
        self.assertIsInstance(cheese_list, list)
        self.assertIsInstance(cheese_list[0], tuple)
        self.assertEqual(len(cheese_list), 5)

    def test_get_initial_mouse_position(self):
        initial_mouse_position = robot_mouse.get_initial_mouse_position(self.grid)
        self.assertIsInstance(initial_mouse_position, list)
        self.assertIsInstance(initial_mouse_position[0], list)
        self.assertEqual(len(initial_mouse_position), 1)
        self.assertEqual(len(initial_mouse_position[0]), 2)

    def test_check_win_status(self):
        self.assertFalse(robot_mouse.check_win_status([]))
        self.assertTrue(robot_mouse.check_win_status([(2, 2)]))

    def test_change_mouse_position(self):
        robot_mouse.change_mouse_position(self.grid, [[2, 2]], [[3, 3]])
        self.assertEqual(
            self.grid,
            [
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', "🧱", "🧱", '🧱', '🧱', '🧱'],
                ['🧱', "🧱", "🧱", '🧱', '🧱', '🧱'],
                ['🧱', '🧱', '🧱', '🐁', '🧱', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
                ['🧱', '🧱', '🧱', '🧱', '🧱', '🧱'],
            ]
        )

    def test_get_mines(self):
        cheese_list = [(3, 3), (4, 4), (5, 5)]
        mine_list = robot_mouse.get_mines(self.grid, cheese_list)
        for mine in mine_list:
            self.assertNotIn(mine, cheese_list)
        self.assertIsInstance(mine_list, list)
        self.assertIsInstance(mine_list[0], tuple)
        self.assertEqual(len(mine_list), 5)
    

    def test_save(self):
        grid = []
        cheese = [] 
        mines = [] 
        mouse_position = []
        health = 5 
        cheese_score = 0
        robot_mouse.save(grid, cheese, mines, mouse_position, health, cheese_score)
        files = os.listdir()
        self.assertIn("game_state.rm", files)

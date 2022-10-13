import os
import time
from random import randint


def get_grid_size() -> int:
    grid_size = input('Grid size?: ')
    
    while not grid_size.isdigit():
        grid_size = input('Grid size?: ')
    return int(grid_size)


def make_grid(grid_size: int):
    grid = []
    for _ in range(grid_size):
        grid.append(["🧱" for _ in range(grid_size)])
    return grid


def initialize_grid(grid: list, cheese_list):
    for h in range(len(grid)):
        for w in range(len(grid)):
            if (h < 1) or (h >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (w < 1) or (w >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (h, w) in cheese_list:
                grid[h][w] = '🧀'


def get_cheese(grid):
    cheese_list = []
    while len(cheese_list) < 5:
        coor = (randint(1, len(grid)-2), randint(1, len(grid)-2))
        
        for _ in grid:
            if coor not in cheese_list:
                cheese_list.append(coor)
    
    return cheese_list


def grid_coordinates(grid: list):
    coordinates = []
    for h in range(len(grid)):
        for w in range(len(grid)):
            coordinates.append((h, w))
    return coordinates


if __name__ == '__main__':
    grid_size = get_grid_size()
    grid = make_grid(grid_size)
    cheese = get_cheese(grid)

    initialize_grid(grid, cheese)

    coordinates = grid_coordinates(grid)
    # alway draw your list at the end
    
    for row in grid:
        for column in row:
            print(column, end='')
        print()
        time.sleep(1)
        os.system("clear")

# 🐁
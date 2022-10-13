import os
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


def initialize_grid(grid: list, cheese_list, initial_mouse_position):
    for h in range(len(grid)):
        for w in range(len(grid)):
            if [h, w] in initial_mouse_position:
                grid[h][w] = '🐁'

            if (h < 1) or (h >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (w < 1) or (w >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (h, w) in cheese_list and grid[h][w] != '🐁':
                grid[h][w] = '🧀'


def get_cheese(grid):
    cheese_list = []
    while len(cheese_list) < 5:
        coor = (randint(1, len(grid)-2), randint(1, len(grid)-2))
        
        for _ in grid:
            if coor not in cheese_list:
                cheese_list.append(coor)
    
    return cheese_list


def get_mines(grid):
    pass


def grid_coordinates(grid: list):
    coordinates = []
    for h in range(len(grid)):
        for w in range(len(grid)):
            coordinates.append((h, w))
    return coordinates


def display_grid(grid: list, health=5, cheese_score=5):
    os.system("clear")
    print("life: "+"💖"*health)
    print("cheese: "+"🧀"*cheese_score, '\n')
    for row in grid:
        for column in row:
            print(column, end='')
        print()


def get_initial_mouse_position():
    return [[randint(1, len(grid)-2), randint(1, len(grid)-2)]]


def change_mouse_position(grid, mouse_position):
    grid[mouse_position[0][0]][mouse_position[0][1]] = '🧱'
    direction = input("Enter move direction right(R), left(L), Up(U), Down(D): ").lower()

    if direction == 'exit' or direction == 'quit':
        quit()

    steps = None

    while steps is None:
        try:
            steps = int(input("Enter number of steps: "))
        except Exception as e:
            pass

    if direction == 'u':
        if mouse_position[0][0] - steps > 0:
            mouse_position[0][0] -= steps

    if direction == 'd':
        if mouse_position[0][0] + steps < len(grid) - 1:
            mouse_position[0][0] += steps
    if direction == 'l':
        if mouse_position[0][1] - steps > 0:
            mouse_position[0][1] -= steps

    if direction == 'r':
        if mouse_position[0][1] + steps < len(grid) - 1:
            mouse_position[0][1] += steps
    grid[mouse_position[0][0]][mouse_position[0][1]] = '🐁'
    return mouse_position


def update_mouse_info(position, cheese, cheese_score, health, mines=None, reward=None):
    if tuple(position[0]) in cheese:
        cheese_score += 1
        cheese.remove(tuple(position[0]))
    return cheese_score, cheese


def check_win_status(cheese):
    if len(cheese) == 0:
        return False
    return True


if __name__ == '__main__':
    grid_size = get_grid_size()
    grid = make_grid(grid_size)
    cheese = get_cheese(grid)
    mouse_position = get_initial_mouse_position()
    health = 5
    cheese_score = 0

    initialize_grid(grid, cheese, mouse_position)

    coordinates = grid_coordinates(grid)
    # alway draw your list at the end
    
    while check_win_status(cheese):
        display_grid(grid, health, cheese_score)
        mouse_position = change_mouse_position(grid, mouse_position)
        cheese_score, cheese = update_mouse_info(mouse_position, cheese, cheese_score, health, mines=None, reward=None)
    display_grid(grid, health, cheese_score)
    print("Congratulations, you won!")
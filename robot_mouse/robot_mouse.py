import os
import time
from random import randint


def get_grid_size() -> int:
    """
    Get input from user for size of the grid
    """
    grid_size = input('Grid size?: ')
    
    while not grid_size.isdigit():
        grid_size = input('Grid size?: ')
    return int(grid_size)


def make_grid(grid_size: int):
    """
    Creates nxn grid using grid_size and 🧱

    :param grid_size: int, used to create square grid

    :return: list, grid filled with 🧱
    """
    grid = []
    for _ in range(grid_size):
        grid.append(["🧱" for _ in range(grid_size)])
    return grid


def initialize_grid(grid: list, cheese_list, initial_mouse_position):
    """
    Creates boundaries of the grid, fills in the 🧀, and spawns the 🐁

    :param grid: list
    :param cheese_list: list, tuple
    :param initial_mouse_position: list, tuple 
    """
    for h in range(len(grid)):
        for w in range(len(grid)):
            if [h, w] in initial_mouse_position and grid[h][w] != '🧀':
                grid[h][w] = '🐁'

            if (h < 1) or (h >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (w < 1) or (w >= len(grid) - 1):
                grid[h][w] = '🟥'
            if (h, w) in cheese_list and grid[h][w] != '🐁':
                grid[h][w] = '🧀'


def get_cheese(grid):
    """
    Creates 2 value coordinates of tuples and puts them inside a list

    :param grid: list

    :return: list, a list that contains 2 value tuples
    """
    cheese_list = []
    while len(cheese_list) < 5:
        coor = (randint(1, len(grid)-2), randint(1, len(grid)-2))
        
        for _ in grid:
            if coor not in cheese_list:
                cheese_list.append(coor)

    return cheese_list


def get_mines(grid, cheese_list):
    """
    Creates 2 value coordinates of tuples and puts them inside a list.
    Makes sure that the coordinates created don't already exist in cheese_list.

    :param grid: list
    :param cheese_list: list

    :return: list, a list that contains 2 value tuples
    """
    mine_list = []
    while len(mine_list) < 5:
        coord = (randint(1, len(grid)-2), randint(1, len(grid)-2))
        
        for _ in grid:
            if coord not in mine_list and coord not in cheese_list:
                mine_list.append(coord)
    return mine_list


def place_remove_mine(grid, mine_position, place=True):
    """
    Removes or places mines on the display.

    :param grid: list, contains the grid being manipulated
    :param mine_position: list, containes 2 value tuples that are mines coordinates
    :param place: bool, determines whether a mine is placed or removed.
    """
    if place:
        grid[mine_position[0][0]][mine_position[0][1]] = '💥'
    else:
        grid[mine_position[0][0]][mine_position[0][1]] = '🧱'


def display_grid(grid: list, health=5, cheese_score=5):
    """
    Creates the display and updates it.
    Clears the console each time before displaying anything.

    :param grid: list, grid used to display the boundaries
    :param health: int, used to track and display the users health
    :param cheese_score: int, used to track and display the users score
    """
    os.system("clear")
    print("life: "+"💖"*health)
    print("cheese: "+"🧀"*cheese_score, '\n')
    for row in grid:
        for column in row:
            print(column, end='')
        print()


def get_direction_and_steps():
    """
    Asks the user the direction they want to go to and the number of steps they want to take

    :return: str, int: returns a string containing direction and integer containing number of steps
    """
    direction = input("Enter move direction right(R), left(L), Up(U), Down(D): ").lower()
    while direction not in ['r', 'l', 'u', 'd']:
        direction = input("Enter move direction right(R), left(L), Up(U), Down(D): ").lower()
        if direction == 'exit' or direction == 'quit':
            quit()

    steps = None
    while steps is None:
        try:
            steps = int(input("Enter number of steps: "))
        except Exception as e:
            pass
    return direction, steps


def get_initial_mouse_position(grid):
    """
    Randomly generates the initial position of the mouse on the grid.

    :param grid: list, used to control the range of random guesses

    :return: list, contains a 2 value list for the initial mouse coordinates
    """
    return [[randint(1, len(grid)-2), randint(1, len(grid)-2)]]


def get_new_mouse_position(grid, mouse_position):
    """
    Asks the user where they want to move the mouse, 
    it also forces the user to stay within boundaries

    :param grid: list, used to control the user from going beyond the boundaries
    :param mouse_position, used to create new mouse position
    """
    old_mouse_position = [mouse_position[0].copy()]
    direction, steps = get_direction_and_steps()
    out_of_bound_message = "Mouse can't be out of bounds!"

    if direction == 'u':
        if mouse_position[0][0] - steps > 0:
            mouse_position[0][0] -= steps
        else:
            print(out_of_bound_message)

    if direction == 'd':
        if mouse_position[0][0] + steps < len(grid) - 1:
            mouse_position[0][0] += steps
        else:
            print(out_of_bound_message)
    if direction == 'l':
        if mouse_position[0][1] - steps > 0:
            mouse_position[0][1] -= steps
        else:
            print(out_of_bound_message)

    if direction == 'r':
        if mouse_position[0][1] + steps < len(grid) - 1:
            mouse_position[0][1] += steps
        else:
            print(out_of_bound_message)
    time.sleep(1)
    return old_mouse_position, mouse_position, direction


def change_mouse_position(grid, old_mouse_position, new_mouse_position):
    grid[old_mouse_position[0][0]][old_mouse_position[0][1]] = '🧱'
    grid[new_mouse_position[0][0]][new_mouse_position[0][1]] = '🐁'


def update_mouse_info(grid, old_mouse_position, mouse_position, direction, cheese, cheese_score, health, mines, reward=None):
    while old_mouse_position != mouse_position:
        prev_old_mouse_position = [old_mouse_position[0].copy()]
        if direction == 'u':
            old_mouse_position[0][0] -= 1
        elif direction == 'd':
            old_mouse_position[0][0] += 1
        elif direction == 'l':
            old_mouse_position[0][1] -= 1
        elif direction == 'r':
            old_mouse_position[0][1] += 1

        if tuple(old_mouse_position[0]) in cheese:
            cheese_score += 1
            cheese.remove(tuple(old_mouse_position[0]))

        if tuple(old_mouse_position[0]) in mines:
            health -= 1
            mouse_position = [prev_old_mouse_position[0].copy()]
            mines.remove(tuple(old_mouse_position[0]))
            place_remove_mine(grid, old_mouse_position)
            display_grid(grid, health, cheese_score)
            time.sleep(0.5)
            place_remove_mine(grid, old_mouse_position, place=False)
            display_grid(grid, health, cheese_score)
            break
        change_mouse_position(grid, prev_old_mouse_position, old_mouse_position)
        display_grid(grid, health, cheese_score)
        time.sleep(0.3)
    return cheese_score, health, mouse_position


def check_win_status(cheese):
    if len(cheese) == 0:
        print("Congratulations, you won!")
        return False
    return True


def check_lose_status(mines):
    if len(mines) == 0:
        print("Sorry, you lost!")
        return False
    return True


if __name__ == '__main__':
    grid_size = get_grid_size()
    grid = make_grid(grid_size)
    cheese = get_cheese(grid)
    mines = get_mines(grid, cheese)
    mouse_position = get_initial_mouse_position(grid)
    health = 5
    cheese_score = 0

    initialize_grid(grid, cheese, mouse_position)
    
    display_grid(grid, health, cheese_score)
    while check_win_status(cheese) and check_lose_status(mines):
        old_mouse_position, mouse_position, direction = get_new_mouse_position(grid, mouse_position)
        cheese_score, health, mouse_position = update_mouse_info(
            grid, 
            old_mouse_position, 
            mouse_position, 
            direction, 
            cheese, 
            cheese_score, 
            health, 
            mines, 
            reward=None
        )
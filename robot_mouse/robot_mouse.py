import os
import time
import pickle
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


def get_direction_and_steps(grid, cheese, mines, mouse_position, health, cheese_score):
    """
    Asks the user the direction they want to go to and the number of steps they want to take

    :return: str, int: returns a string containing direction and integer containing number of steps
    """
    direction = ""
    while direction not in ['r', 'l', 'u', 'd']:
        direction = input("Enter move direction right(R), left(L), Up(U), Down(D), Save(S), quit(Q): ").lower()
        if direction == 'exit' or direction == 'q':
            quit()
        
        if direction == "s":
            save(grid, cheese, mines, mouse_position, health, cheese_score)

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


def get_new_mouse_position(grid, cheese, mines, mouse_position, health, cheese_score):
    """
    Asks the user where they want to move the mouse, 
    it also forces the user to stay within boundaries

    :param grid: list, used to control the user from going beyond the boundaries
    :param mouse_position, used to create new mouse position
    """
    old_mouse_position = [mouse_position[0].copy()]
    direction, steps = get_direction_and_steps(grid, cheese, mines, mouse_position, health, cheese_score)
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
    """
    Changes mouse position from old position to new position.
    Replaces old mouse position on the grid with 🧱, places 🐁 on the new mouse position on the grid.

    :param grid: list, where 🧱, 🐁 are moved and placed
    :param old_mouse_position: list, contains a 2 value list representing old mouse coordinates
    :param new_mouse_position: list, contains a 2 value list representing new mouse coordinates
    """
    grid[old_mouse_position[0][0]][old_mouse_position[0][1]] = '🧱'
    grid[new_mouse_position[0][0]][new_mouse_position[0][1]] = '🐁'


def update_mouse_info(grid, old_mouse_position, mouse_position, direction, cheese, cheese_score, health, mines):
    """
    Tracks the path the mouse took when moving and determines if it did or didn't hit any cheese or mines,
    and if did hit a cheese or a mine it increases the score or decreases the mouse's health

    :param grid: list, used as argument when calling change_mouse_position, and display grid function
    :param old_mouse_position: list, contains a 2 value list representing old mouse coordinates
    :param new_mouse_position: list, contains a 2 value list representing new mouse coordinates
    :param direction: str, contains the direction the user choice to move
    :param cheese: list, contains 2 value tuples representing all of the cheeses coordinates
    :param cheese_score: int, used to track users score
    :param health: int, used to track mouses health
    :param mines: list, contains 2 value tuples representing all of the mines 
    
    :return: int, int, list
    """
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
    """
    Checks if the user has won the game.

    :param cheese: list, used to track if there are any cheese coordinates left

    :return: bool, if there are no cheese coordinates left it returns False and a message congratulating the user for winning
                 , otherwise it returns True
    """
    if len(cheese) == 0:
        print("Congratulations, you won!")
        return False
    return True


def check_lose_status(mines):
    """
    Checks if the user has lost the game.

    :param mines: list, used to track if there are any mines coordinates left

    :return: bool, if there are no mines coordinates left it returns False and a message telling the user that they lost
                 , otherwise it returns True
    """
    if len(mines) == 0:
        print("Sorry, you lost!")
        return False
    return True


def save(grid, cheese, mines, mouse_position, health, cheese_score):
    with open("game_state.rm", "wb") as f:
        game_state = [
            grid,
            cheese,
            mines,
            mouse_position,
            health,
            cheese_score
        ]
        pickle.dump(game_state, f)
    print("Game saved!")
    quit()


def load():
    files = os.listdir()
    for file in files:
        if file[-2:] == "rm":
            with open(file, "rb") as f:
                game_state = pickle.load(f)
                return game_state


def load_saved_game():
    user_response = input("Load saved game? (y/n): ").lower()
    
    if user_response == "n":
        return False
    else:
        files = os.listdir()
        for file in files:
            if file[-2:] == "rm":
                return True


if __name__ == '__main__':
    if load_saved_game():
        grid, cheese, mines, mouse_position, health, cheese_score = load()
    else:
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
        old_mouse_position, mouse_position, direction = get_new_mouse_position(
            grid, 
            cheese, 
            mines, 
            mouse_position, 
            health, 
            cheese_score
        )
        cheese_score, health, mouse_position = update_mouse_info(
            grid, 
            old_mouse_position, 
            mouse_position, 
            direction, 
            cheese, 
            cheese_score, 
            health, 
            mines
        )
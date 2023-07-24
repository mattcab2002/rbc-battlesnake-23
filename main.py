# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


def flood_fill(game_state: typing.Dict, open_squares, explored):
    current_head = game_state["you"]["head"]
    x = current_head["x"]
    y = current_head["y"]
    queue = [current_head]
    # add node to queue
    while len(queue) > 0:
        n = queue[0]  # dequeue
        queue = queue[1:]
        if y == n["y"]:
            if x < n["x"]:
                open_squares["right"] += 1
            elif x > n["x"]:
                open_squares["left"] += 1
        if x == n["x"]:
            if y < n["y"]:
                open_squares["up"] += 1
            elif y > n["y"]:
                open_squares["down"] += 1

        queue.extend(available_positions(n, game_state, explored))
        explored.append(n)
    return open_squares


def available_positions(position, game_state, explored):
    lst_to_return = []
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    if position not in explored:
        if position["y"] != board_height - 1 and {"x": position["x"], "y": position["y"] + 1} not in explored and not (my_neck["y"] > my_head["y"]):
            lst_to_return.append({"x": position["x"], "y": position["y"] + 1})
        if position["y"] != 0 and {"x": position["x"], "y": position["y"] - 1} not in explored and not (my_neck["y"] < my_head["y"]):
            lst_to_return.append({"x": position["x"], "y": position["y"] - 1})
        if position["x"] != 0 and {"x": position["x"] - 1, "y": position["y"]} not in explored and not (my_neck["x"] < my_head["x"]):
            lst_to_return.append({"x": position["x"] - 1, "y": position["y"]})
        if position["x"] != board_width - 1 and {"x": position["x"] + 1, "y": position["y"]} not in explored and not (my_neck["x"] > my_head["x"]):
            lst_to_return.append({"x": position["x"] + 1, "y": position["y"]})
    return lst_to_return

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Quebek Snek",  # TODO: Your Battlesnake Username
        "color": "#003399",  # Quebec Flag Color
        "head": "earmuffs",
        "tail": "flake",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print(game_state)
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    head = my_body[0]

    temp = head.copy()
    temp["x"] += 1
    if temp in my_body[1:] and my_body[1:].index(temp) != len(
            my_body) - 1:  # if body part not already there and is not tail
        is_move_safe["right"] = False

    temp = head.copy()
    temp["x"] -= 1
    if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
        is_move_safe["left"] = False

    temp = head.copy()
    temp["y"] += 1
    if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
        is_move_safe["up"] = False

    temp = head.copy()
    temp["y"] -= 1
    if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
        is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    # below are debug lines to move in the direction with the max available space
    # directions = flood_fill(game_state, {"left": 0, "right": 0, "up": 0, "down": 0},[])
    # return {"move": list(directions.keys())[list(directions.values()).index(max(list(directions.values())))]}

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})

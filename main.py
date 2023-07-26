import random
import typing

#import board
#import logic

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
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

  #curBoard = board.Board(game_state["board"])
  #headPosition = game_state["you"]["body"][0]
  health = game_state["you"]["health"]

  #logic.getBestMove(curBoard, headPosition, health)

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

  temp = my_head.copy()
  temp["x"] += 1
  if temp in my_body[1:] and my_body[1:].index(temp) != len(
      my_body) - 1:  # if body part not already there and is not tail
    is_move_safe["right"] = False

  temp = my_head.copy()
  temp["x"] -= 1
  if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
    is_move_safe["left"] = False

  temp = my_head.copy()
  temp["y"] += 1
  if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
    is_move_safe["up"] = False

  temp = my_head.copy()
  temp["y"] -= 1
  if temp in my_body[1:] and my_body[1:].index(temp) != len(my_body) - 1:
    is_move_safe["down"] = False

  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']

  snake_bodies = []
  snake_heads = []
  for snake in opponents:
    if snake['id'] != game_state['you']['id']:
      snake_heads.append([snake['head'], snake['length']])
      snake_bodies.append(snake['body'])
  
  for body in snake_bodies:
    for part in body:
      if (my_head["x"]-part["x"]) == 2 and (my_head["y"]-part["y"]) == 0 :
        is_move_safe["left"] = False
      if (my_head["x"]-part["x"]) == -2 and (my_head["y"]-part["y"]) == 0 :
        is_move_safe["right"] = False
      if (my_head["y"]-part["y"]) == 2 and (my_head["x"]-part["x"]) == 0 :
        is_move_safe["down"] = False
      if (my_head["y"]-part["y"]) == -2 and (my_head["x"]-part["x"]) == 0 :
        is_move_safe["up"] = False

  # Flood Fill Checks
  directions = flood_fill(game_state, {"left": 0, "right": 0, "up": 0, "down": 0},[])
  if health > 50:
    current_max = 0
    for (key, value) in is_move_safe.items(): # find current move which is safe and has max value
        if value == True and directions[key] > current_max and enough_space(game_state, directions, key) == True:
            current_max = directions[key]
    for (key, value) in directions.items():
        if value < current_max:
            is_move_safe[key] = False

  # Are there any safe moves left?
  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    return {"move": "down"}

  # Choose a random move from the safe ones
  next_move = random.choice(safe_moves)

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  food = game_state['board']['food']
  foodDistance = []
  for item in food:
    foodDistance.append(
      abs(my_head["x"] - item["x"]) + abs(my_head["y"] - item["y"]))
  # find the nearest food location
  smallestDistance = foodDistance.index(min(foodDistance))
  # plan the route to food
  if ("right" in safe_moves
      and my_head["x"] - food[smallestDistance]["x"] < 0):
    next_move = "right"
  elif ("left" in safe_moves
        and my_head["x"] - food[smallestDistance]["x"] > 0):
    next_move = "left"
  elif ("up" in safe_moves and my_head["y"] - food[smallestDistance]["y"] < 0):
    next_move = "up"
  elif ("down" in safe_moves
        and my_head["y"] - food[smallestDistance]["y"] > 0):
    next_move = "down"

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}

def enough_space(game_state, directions, desired_move):
    while True:
        if desired_move == "left":
            new_game_state = game_state.copy()
            new_game_state["you"]["head"]["x"] -= 1
        elif desired_move == "right":
            new_game_state = game_state.copy()
            new_game_state["you"]["head"]["x"] += 1
        elif desired_move == "up":
            new_game_state = game_state.copy()
            new_game_state["you"]["head"]["y"] += 1
        elif desired_move == "down":
            new_game_state = game_state.copy()
            new_game_state["you"]["head"]["y"] -= 1
        result = flood_fill(game_state, {"left": 0, "right": 0, "up": 0, "down": 0},[])

        board_width = game_state['board']['width']
        board_height = game_state['board']['height']
        my_head = new_game_state["you"]["head"]

        if my_head["y"] == board_height - 1 or my_head["y"] == 0 or my_head["x"] == 0 or my_head["x"] == board_width - 1:
            break
    for value in result.values():
        if value > 0:
            return True
    return False
    

# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})

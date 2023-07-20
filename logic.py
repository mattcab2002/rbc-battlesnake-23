#Utilities
def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])



#
def getBestMove(board,headPosition,health):
  
  # start with general area
  direction = {
    "up": 100 / (distance(headPosition, (headPosition[0], 0)) + 1),
    "down": 100 / (distance(headPosition, (headPosition[0], board.height)) + 1),
    "right": 100 / (distance((board.width, headPosition[1]), headPosition) + 1),
    "left": 100 / (distance((0, headPosition[1]), headPosition) + 1)
  }
  # Bottom Left is 0,0 
  
    # close to a border or snake?
  if not board.vacant((headPosition[0]-1,headPosition[1])):
      direction["left"] += 1000000

  if not board.vacant((headPosition[0]+1,headPosition[1])):
      direction["right"] += 1000000

  if not board.vacant((headPosition[0],headPosition[1]-1)):
      direction["up"] += 1000000

  if not board.vacant((headPosition[0],headPosition[1]+1)):
      direction["down"] += 1000000
  

  
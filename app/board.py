class Board():
  def __init(self,**gameState):
    self.width = gameState['width']
    self.height = gameState['height']
    self.food = list(map(tuple, gameState['food']))


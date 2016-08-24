from square import Square
from gamestatechange import GameStateChange

class FreeSpace(Square):
	def __init__(self, name):
		super(FreeSpace, self).__init__(name)

	def landed(self, player, roll, state):
		return GameStateChange()
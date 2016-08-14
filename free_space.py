from square import Square
from gamestatechange import GameStateChange

class FreeSpace(Square):
	def __init__(self):
		pass

	def landed(self, player, roll, state):
		return GameStateChange()
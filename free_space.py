from square import Square
from gamestatechange import GameStateChange

class FreeSpace(Square):
	def __init__(self):
		pass

	def landed(self, player, state):
		return GameStateChange()
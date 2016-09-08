from square import Square
from groupofchanges import GroupOfChanges

class FreeSpace(Square):
	def __init__(self, name):
		super(FreeSpace, self).__init__(name)

	def landed(self, player, roll, state):
		return GroupOfChanges()